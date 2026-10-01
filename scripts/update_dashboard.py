import sys

with open(r"d:\NETRA\SIH2026\src\pages\Dashboard.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject import
content = content.replace(
    "import { fetchWithAuth } from '../api/apiClient';",
    "import { fetchWithAuth } from '../api/apiClient';\nimport { useTranslation } from 'react-i18next';"
)

# 2. Inject hook and logic
hook_code = """const Dashboard = () => {
    const { t, i18n } = useTranslation();
    const toggleLanguage = () => {
        i18n.changeLanguage(i18n.language === 'en' ? 'hi' : 'en');
    };"""
content = content.replace("const Dashboard = () => {", hook_code)

# 3. Replace header language text with a working button
old_button = '<span className="text-label-md font-label-md hidden sm:inline-block">Hindi/English</span>'
new_button = '<button onClick={toggleLanguage} className="text-label-md font-label-md hidden sm:inline-block hover:underline">{t("header.toggle_lang")}</button>'
content = content.replace(old_button, new_button)

# 4. Translate some visible strings
old_title = '<h2 className="text-title-md md:text-title-lg font-headline-lg-mobile md:font-headline-lg text-primary">Dashboard Overview</h2>'
new_title = '<h2 className="text-title-md md:text-title-lg font-headline-lg-mobile md:font-headline-lg text-primary">{t("dashboard.title")}</h2>'
content = content.replace(old_title, new_title)

old_sub = '<p className="text-body-md font-body-md text-on-surface-variant mt-1">Network Analysis &amp; Intelligence Summary</p>'
new_sub = '<p className="text-body-md font-body-md text-on-surface-variant mt-1">{t("dashboard.subtitle")}</p>'
content = content.replace(old_sub, new_sub)

old_stat1 = '<p className="text-label-md font-label-md text-on-surface-variant">Total Cases</p>'
new_stat1 = '<p className="text-label-md font-label-md text-on-surface-variant">{t("dashboard.total_cases")}</p>'
content = content.replace(old_stat1, new_stat1)

old_stat2 = '<p className="text-label-md font-label-md text-on-surface-variant">Flagged Entities</p>'
new_stat2 = '<p className="text-label-md font-label-md text-on-surface-variant">{t("dashboard.flagged_entities")}</p>'
content = content.replace(old_stat2, new_stat2)


with open(r"d:\NETRA\SIH2026\src\pages\Dashboard.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Dashboard.tsx")
