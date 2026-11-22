# Entwurf 14.11.2026 – nicht veröffentlicht. Erklärung:
# docs/10_VEROEFFENTLICHUNG.md#winget-und-homebrew-entwurf
# Gehört in ein eigenes Tap-Repository n05a-design/homebrew-glide (Casks/glide.rb).
# sha256 ist ein Platzhalter: Wert aus Glide-<v>-macos-arm64.dmg.sha256 eintragen.
cask "glide" do
  version "1.0.1"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"

  url "https://github.com/n05a-design/glide-to-do/releases/download/v#{version}/Glide-#{version}-macos-arm64.dmg"
  name "Glide"
  desc "Desktop-Planer für Projekte, Aufgaben, Tagesplanung und Pinnwände"
  homepage "https://github.com/n05a-design/glide-to-do"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  # macOS-Mindestversion ist laut Produktregister noch offen; nach Messung ergänzen,
  # z. B. depends_on macos: ">= :sonoma".

  app "Glide.app"

  # Bewusst ohne ~/Library/Application Support/Glide: Das sind die Nutzerdaten.
  # `brew uninstall --zap` entfernt nur Zwischenspeicher und Systemzustand.
  zap trash: [
    "~/Library/Caches/Glide",
    "~/Library/Preferences/de.shaye.glide.plist",
    "~/Library/Saved Application State/de.shaye.glide.savedState",
  ]

  caveats <<~EOS
    Glide ist noch nicht mit einer Apple Developer ID signiert und notarisiert.
    Beim ersten Start blockiert macOS das Öffnen. Dann unter
      Systemeinstellungen › Datenschutz & Sicherheit
    bei „Glide“ auf „Dennoch öffnen“ klicken.

    Deine Daten liegen unter ~/Library/Application Support/Glide
    und bleiben bei einer Deinstallation erhalten.
  EOS
end
