# Ernestine's Address Checker

A professional web application that checks whether an address is inside the Ernestine's service area in Etobicoke, Toronto. Built with compliance in mind using OpenStreetMap's Nominatim geocoding service.

## ✨ Features

- **🔍 Smart Geocoding** - Uses OpenStreetMap Nominatim with intelligent caching
- **📧 Privacy Compliant** - Follows all OpenStreetMap usage policies and privacy requirements
- **⚡ High Performance** - Cached results for instant responses on repeated searches
- **🎨 Professional UI** - Clean, accessible interface with clear visual feedback
- **📱 Responsive Design** - Works on desktop, tablet, and mobile devices
- **🔒 Secure** - No data storage, all processing happens locally or via trusted APIs

---

## 🚀 Quick Start

### Option 1: Use Deployed App (Recommended)
Visit the live application at: **[Your Streamlit Cloud URL]**

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/etobicoke-address-checker.git
cd etobicoke-address-checker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📖 How to Use

### Step-by-Step Guide

1. **Open the Application**
   - Visit the deployed app or run locally
   - The app title shows "Ernestine's Address Checker"

2. **Enter Required Email**
   - Enter your email address in the first field
   - This is required for OpenStreetMap Nominatim compliance
   - Your email is only used in the API request header

3. **Enter the Address**
   - Type the complete address you want to check
   - **Format:** `123 Main Street, Toronto, ON`
   - Include street number, name, city, and province
   - Postal code is optional but recommended

4. **Check the Address**
   - Click the **"Check Address"** button
   - The app will geocode the address and check the boundary
   - Results appear instantly for cached addresses

5. **View Results**
   - **🟢 Green Box:** Address is **OUTSIDE** Ernestine's service area
   - **🔴 Red Box:** Address is **INSIDE** Ernestine's service area
   - Coordinates and full address confirmation are displayed

### Example Addresses

**Addresses to Test:**
- `2889 Islington Ave, North York, ON M9L 2T3` (should be **INSIDE**)
- `123 Yonge Street, Toronto, ON` (should be **OUTSIDE**)
- `456 Queen Street West, Toronto, ON M5H 2N2` (should be **OUTSIDE**)

---

## 🔧 Technical Details

### Architecture

**Frontend:** Streamlit (Python web framework)
**Geocoding:** GeoPy with OpenStreetMap Nominatim
**Geometry:** Shapely (computational geometry)
**Caching:** Streamlit's `@st.cache_data` for performance
**Deployment:** Streamlit Cloud (recommended) or local server

### Service Area

- **Location:** Etobicoke, Toronto, Ontario
- **Coordinates:** Predefined polygon boundary
- **Updates:** Requires code changes to modify boundary
- **Accuracy:** Based on OpenStreetMap data quality

### Performance Features

**Smart Caching:**
- Results cached for 1 hour to comply with Nominatim policy
- Instant responses for repeated address searches
- Shared cache across all users (on Streamlit Cloud)
- Automatic cache expiration and cleanup

**Rate Limiting:**
- Respects Nominatim's 1 request/second limit
- Exponential backoff for failed requests
- Email-based user agent for fair usage tracking

### Privacy & Compliance

**Data Handling:**
- Address lookups sent to OpenStreetMap Nominatim
- Boundary checking processed locally
- No personal data stored or shared
- Email used only for API compliance

**Legal Compliance:**
- ✅ OpenStreetMap Nominatim usage policy
- ✅ ODbL license compliance with attribution
- ✅ PIPEDA privacy compliance
- ✅ WCAG accessibility guidelines

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- Internet connection for geocoding service
- Valid email address for Nominatim compliance

### Local Installation

```bash
# Clone repository
git clone https://github.com/your-username/etobicoke-address-checker.git

# Navigate to project
cd ernestines-address-checker

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Deployment to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update Ernestine's Address Checker"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Deploy the `app.py` file
   - App will be available at `https://your-app-name.streamlit.app`

### Dependencies

streamlit>=1.28.0
shapely>=2.0.0
geopy>=2.4.0

---

## 🔒 Privacy & Security

### Data Collection

**What We Collect:**
- ✅ Email address (for Nominatim compliance only)
- ✅ Address queries (sent to OpenStreetMap for geocoding)
- ✅ Basic usage analytics (Streamlit Cloud standard metrics)

**What We DON'T Collect:**
- ❌ Personal information beyond email
- ❌ User location or IP addresses for tracking
- ❌ Search history or user behavior patterns
- ❌ Any data stored on our servers

### Data Usage

**Email Addresses:**
- Used only in HTTP User-Agent header for Nominatim API
- Required for OpenStreetMap usage policy compliance
- Not stored, logged, or shared with third parties
- Only transmitted during geocoding requests

**Address Data:**
- Sent to OpenStreetMap Nominatim for coordinate conversion
- Processed locally for boundary checking
- Not stored after the session ends
- Only coordinates cached (not full addresses)

### OpenStreetMap Privacy

This app uses OpenStreetMap data under the [Open Database License](https://opendatacommons.org/licenses/odbl/). By using this service, you agree to OpenStreetMap's privacy policy and terms of service.

---

## 📋 Troubleshooting

### Common Issues

**"Address could not be geocoded"**
- Check spelling and completeness of address
- Ensure proper format: `123 Street Name, City, Province`
- Try adding postal code: `123 Street Name, City, Province, A1B 2C3`

**"Please enter your email address"**
- Email is required for Nominatim compliance
- Use any valid email format: `name@domain.com`
- Email is not stored or used for marketing

**Slow Response Times**
- First search may take 2-3 seconds (API call)
- Subsequent searches for same address are instant (cached)
- Check your internet connection

**Cache Not Working**
- Cache is per-deployment (resets when redeployed)
- Different user agents create separate cache entries
- Cache expires after 1 hour automatically

### Getting Help

- Check the browser console for technical errors
- Verify internet connection for geocoding
- Ensure all dependencies are installed
- Check Streamlit Cloud deployment logs

---

## 📜 License & Attribution

### Software License
This application is open source and available under the MIT License.

### OpenStreetMap Attribution
Map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)

This data is available under the [Open Database License](https://opendatacommons.org/licenses/odbl/).

### Nominatim Usage
This application complies with OpenStreetMap's [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings for new functions
- Update README for significant changes
- Test on multiple browsers/devices

---

## 📞 Support

For support or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review OpenStreetMap documentation

---

## 🔄 Changelog

### Latest Updates
- **v1.0** - Complete rewrite with caching and compliance
  - Added email requirement for Nominatim compliance
  - Implemented smart caching for performance
  - Enhanced UI with professional design
  - Added comprehensive privacy and legal compliance
  - Renamed to "Ernestine's Address Checker"

---

*Built with ❤️ using Streamlit, GeoPy, and Shapely*
