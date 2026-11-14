// Standalone Foundation client: proves HTTP + decoding, not installed Seagis UI.
import Foundation

struct SSTRow: Decodable {
    let validAt: String
    let value: Double?
    let valueStatus: String
}

struct SSTCell: Decodable {
    let latitude: Double
    let longitude: Double
    let depthM: Double
}

struct SSTResponse: Decodable {
    let schemaVersion: String
    let mode: String
    let plotId: String
    let trainingAuthorized: Bool
    let farmFallbackAuthorized: Bool
    let scope: String
    let dataset: String
    let variable: String
    let unit: String
    let nativeCadenceSeconds: Int
    let temporalStatistic: String
    let temporalStatus: String
    let spatialSupport: String
    let coordinateStatus: String
    let lastCheckedAt: String
    let providerUpdatedAt: String?
    let contentRevision: String
    let current: SSTRow?
    let cell: SSTCell
    let rows: [SSTRow]
}

enum ProbeError: Error { case invalidArguments, invalidHTTP, invalidPayload }

@main struct AppProbe {
    static func main() async throws {
        guard CommandLine.arguments.count == 3,
              let endpoint = URL(string: CommandLine.arguments[1]) else {
            throw ProbeError.invalidArguments
        }
        let expectedPlot = CommandLine.arguments[2]
        // HTTP only for a local probe. Production must use HTTPS and app auth.
        guard endpoint.scheme == "https" ||
                (endpoint.scheme == "http" && endpoint.host == "127.0.0.1") else {
            throw ProbeError.invalidArguments
        }
        var request = URLRequest(url: endpoint)
        request.cachePolicy = .reloadIgnoringLocalCacheData
        request.timeoutInterval = 20
        let (data, response) = try await URLSession.shared.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 200 else {
            throw ProbeError.invalidHTTP
        }
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let dto = try decoder.decode(SSTResponse.self, from: data)
        guard dto.schemaVersion == "sst-probe-1", dto.mode == "feasibility_probe",
              dto.plotId == expectedPlot,
              !dto.trainingAuthorized, !dto.farmFallbackAuthorized,
              dto.scope == "regional_model", dto.variable == "thetao", dto.unit == "degC",
              dto.nativeCadenceSeconds == 3600, dto.temporalStatistic == "hourly_mean",
              dto.spatialSupport == "unverified", !dto.rows.isEmpty else {
            throw ProbeError.invalidPayload
        }
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime]
        var previous: Date?
        for row in dto.rows {
            guard let date = formatter.date(from: row.validAt),
                  row.value?.isFinite ?? true,
                  (row.valueStatus == "present" && row.value != nil) ||
                    (row.valueStatus == "missing" && row.value == nil) else {
                throw ProbeError.invalidPayload
            }
            if let previous, date.timeIntervalSince(previous) != 3600 {
                throw ProbeError.invalidPayload
            }
            previous = date
        }
        if let current = dto.current {
            let hour = floor(Date().timeIntervalSince1970 / 3600) * 3600
            guard formatter.date(from: current.validAt)?.timeIntervalSince1970 == hour else {
                throw ProbeError.invalidPayload
            }
        }
        let result: [String: Any] = [
            "result": "http_decode_passed", "plot_id": dto.plotId,
            "sample_count": dto.rows.count, "unit": dto.unit,
            "temporal_status": dto.temporalStatus,
            "current_valid_at": dto.current?.validAt as Any? ?? NSNull(),
            "current_value": dto.current?.value as Any? ?? NSNull(),
            "coordinate_status": dto.coordinateStatus,
            "cell_latitude": dto.cell.latitude, "cell_longitude": dto.cell.longitude,
            "content_revision": dto.contentRevision,
            "production_app_integrated": false
        ]
        let json = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
        print(String(decoding: json, as: UTF8.self))
    }
}
