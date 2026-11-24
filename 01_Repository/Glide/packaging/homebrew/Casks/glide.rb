# Entwurf 14.11.2026 – nicht veröffentlicht. Erklärung:
# docs/10_VEROEFFENTLICHUNG.md#winget-und-homebrew-entwurf
# Gehört in ein eigenes Tap-Repository n05a-design/homebrew-glide (Casks/glide.rb).
# sha256 ist verifiziert für v1.0.2 (aus Glide-1.0.2-macos-arm64.dmg.sha256).
cask "glide" do
  version "1.0.2"
  sha256 "1aeb2247b60384dca14b19fd93147a5d5819b4bc4134948adea33ff88e43b7cc"

  url "https://github.com/n05a-design/glide-to-do/releases/download/v#{version}/Glide-#{version}-macos-arm64.dmg"
  name "Glide"
  desc "Desktop-Planer für Projekte, Aufgaben, Tagesplanung und Pinnwände"
  homepage "https://github.com/n05a-design/glide-to-do"

  livecheck do
    url :url
    strategy :github_latest
    # Hinweis: Bei GitHub-Prereleases greift :github_latest erst, sobald ein volles
    # Stable-Release publiziert wird. Alternativ kann auf GitHub-Releases geprüft werden.
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
