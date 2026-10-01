import Foundation
import CryptoKit
struct Entry: Decodable {let path: String; let sha256: String}
let entries = try JSONDecoder().decode([Entry].self, from: Data(contentsOf: URL(fileURLWithPath: "/tmp/glide-cleanup-list.json")))
var removed: [String] = []
var errors: [String] = []
for (index, entry) in entries.enumerated() {
 let url = URL(fileURLWithPath: entry.path)
 guard FileManager.default.fileExists(atPath: entry.path) else { continue }
 do {
  let digest = SHA256.hash(data: try Data(contentsOf: url)).map {String(format: "%02x", $0)}.joined()
  guard digest == entry.sha256 else {errors.append("Changed content: " + entry.path);continue}
  try FileManager.default.trashItem(at: url, resultingItemURL: nil)
  removed.append(entry.path)
 } catch {errors.append(entry.path + ": " + String(describing:error))}
 if index % 100 == 0 {print("Processed \(index) of \(entries.count)")}
}
let result: [String:Any] = ["removed":removed,"errors":errors,"method":"FileManager.trashItem with original SHA-256 guard"]
try JSONSerialization.data(withJSONObject: result, options:[.prettyPrinted,.sortedKeys]).write(to: URL(fileURLWithPath: "/tmp/glide-cleanup-result.json"))
print("Removed \(removed.count); errors \(errors.count)")
