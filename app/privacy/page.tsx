"use client";

import { useState } from "react";

const content = {
  nl: {
    heading: "Privacybeleid",
    updated: "Laatst bijgewerkt: 7 november 2026",
    sections: [
      ["1. Inleiding", "De Bijbel na ini Sranan Tongo is een digitaal Bijbelplatform van Good News Suriname, verbonden aan Stichting BIMI Suriname. Dit beleid geldt voor srananbijbel.org en de Android-app. Het zal ook gelden voor een toekomstige iOS-app zodra deze beschikbaar is en de beschreven werkwijze overeenkomt met die app."],
      ["2. Persoonsgegevens en contact", "Voor het lezen van de Bijbel is geen account of registratie vereist. Wij vragen daarbij niet om uw naam, e-mailadres of telefoonnummer. Als u ons vrijwillig e-mailt, ontvangen en verwerken wij uw e-mailadres en de inhoud van uw bericht om te kunnen antwoorden."],
      ["3. Lokale opslag", "De website en app kunnen taal- en weergavevoorkeuren, leespositie, instellingen en gedownloade Bijbelvertalingen of commentaren op uw apparaat opslaan. Deze gegevens ondersteunen de werking van het platform en offline gebruik. Wij gebruiken deze lokale gegevens niet voor advertenties of profilering. U kunt lokale gegevens doorgaans wissen via uw browser- of apparaatinstellingen."],
      ["4. Hosting en internetverzoeken", "Onze website wordt gehost door Vercel. Wanneer u de website bezoekt of wanneer de app inhoud ophaalt van srananbijbel.org, kunnen Vercel en betrokken infrastructuurproviders technische gegevens verwerken, zoals IP-adres, tijdstip en opgevraagde bestanden, om verzoeken af te handelen en de dienst te beveiligen. Wij gebruiken deze gegevens niet om individuele lezers te profileren."],
      ["5. Analyse en advertenties", "Het platform bevat geen advertenties. Wij gebruiken momenteel geen Google Analytics, Firebase Analytics of Vercel Web Analytics om bezoekersgedrag te analyseren. Wij verkopen geen persoonsgegevens en gebruiken deze niet voor gerichte advertenties."],
      ["6. Externe links en delen", "Het platform kan links bevatten naar externe websites, video's of bronnen. Externe aanbieders hanteren hun eigen privacybeleid. Wanneer u zelf Bijbelteksten deelt via de deelfunctie van uw apparaat, bepaalt u welke app of dienst de inhoud ontvangt."],
      ["7. Kinderen", "Het platform is bedoeld voor een breed publiek, waaronder gezinnen en kinderen. Er is geen registratie vereist. Wij verzamelen niet bewust persoonsgegevens van kinderen voor marketing of profilering."],
      ["8. Beveiliging en bewaartermijnen", "Wij nemen redelijke maatregelen om onze diensten te beveiligen. Lokale gegevens blijven doorgaans bewaard totdat u ze verwijdert of de opslag wist. Hostingproviders kunnen technische gegevens bewaren volgens hun toepasselijke bewaartermijnen. E-mailcorrespondentie bewaren wij zolang redelijkerwijs nodig is voor beantwoording, administratie of wettelijke verplichtingen."],
      ["9. Wijzigingen", "Wij kunnen dit beleid bijwerken wanneer functies of gegevensverwerking veranderen. De actuele versie staat op https://srananbijbel.org/privacy."],
      ["10. Contact", "Good News Suriname · Stichting BIMI Suriname · Paramaribo, Suriname · srananbijbel@gmail.com"],
    ],
  },
  en: {
    heading: "Privacy Policy",
    updated: "Last updated: November 7, 2026",
    sections: [
      ["1. Introduction", "De Bijbel na ini Sranan Tongo is a digital Bible platform provided by Good News Suriname, associated with Stichting BIMI Suriname. This policy covers srananbijbel.org and the Android application. It is also intended to cover a future iOS application once released, provided its practices match those described here."],
      ["2. Personal information and contact", "No account or registration is required to read the Bible. We do not ask for your name, email address, or phone number for ordinary reading. If you voluntarily email us, we receive and process your email address and message to respond."],
      ["3. Local storage", "The website and app may save language and display preferences, reading position, settings, and downloaded Bible translations or commentaries on your device. These support the service and offline access. We do not use this locally stored information for advertising or profiling. You can generally clear local data through your browser or device settings."],
      ["4. Hosting and internet requests", "Our website is hosted by Vercel. When you visit the website or the app retrieves content from srananbijbel.org, Vercel and relevant infrastructure providers may process technical information such as IP address, request time, and requested resources to deliver and secure the service. We do not use this information to profile individual Bible readers."],
      ["5. Analytics and advertising", "The platform does not display advertisements. We do not currently use Google Analytics, Firebase Analytics, or Vercel Web Analytics to analyze visitor behavior. We do not sell personal information or use it for targeted advertising."],
      ["6. External links and sharing", "The platform may link to external websites, videos, or resources. External providers have their own privacy policies. When you choose to share Scripture using your device's sharing function, you decide which application or service receives it."],
      ["7. Children's privacy", "The platform is intended for a general audience, including families and children. Registration is not required. We do not knowingly collect children's personal information for marketing or profiling."],
      ["8. Security and retention", "We take reasonable measures to secure our services. Local data generally remains until you delete it or clear the relevant storage. Hosting providers may retain technical information under their applicable retention practices. We retain email correspondence for as long as reasonably needed to respond, maintain records, or comply with legal obligations."],
      ["9. Changes", "We may update this policy when features or data practices change. The current version is available at https://srananbijbel.org/privacy."],
      ["10. Contact", "Good News Suriname · Stichting BIMI Suriname · Paramaribo, Suriname · srananbijbel@gmail.com"],
    ],
  },
} as const;

export default function PrivacyPage() {
  const [language, setLanguage] = useState<"nl" | "en">("nl");
  const policy = content[language];
  return (
    <main style={{ maxWidth: 820, margin: "0 auto", padding: "48px 20px 80px", lineHeight: 1.75, fontFamily: "system-ui, sans-serif", color: "#20242a" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
        <a href="/" style={{ color: "#235b48" }}>← De Bijbel na ini Sranan Tongo</a>
        <div aria-label="Language / Taal">
          <button type="button" onClick={() => setLanguage("nl")} aria-pressed={language === "nl"} style={{ padding: "8px 12px", fontWeight: language === "nl" ? 700 : 400 }}>Nederlands</button>
          <button type="button" onClick={() => setLanguage("en")} aria-pressed={language === "en"} style={{ padding: "8px 12px", fontWeight: language === "en" ? 700 : 400 }}>English</button>
        </div>
      </div>
      <h1 style={{ fontSize: "2rem", marginTop: 32 }}>{policy.heading}</h1>
      <p><strong>De Bijbel na ini Sranan Tongo</strong><br />Good News Suriname | Stichting BIMI Suriname</p>
      <p style={{ color: "#555" }}>{policy.updated}</p>
      {policy.sections.map(([title, body]) => (
        <section key={title} style={{ marginTop: 30 }}>
          <h2 style={{ fontSize: "1.25rem", marginBottom: 8 }}>{title}</h2>
          <p>{body}</p>
          {title.startsWith("10.") && <p><a href="mailto:srananbijbel@gmail.com">srananbijbel@gmail.com</a></p>}
        </section>
      ))}
    </main>
  );
}
