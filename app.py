import streamlit as st
from shapely.geometry import Point, Polygon
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import re

# -------------------------------
# Polygon coordinates (Etobicoke area)
boundary_coords = [
    [
              -79.55463119685356,
              43.71442404640791
            ],
            [
              -79.55234355716034,
              43.70945856801646
            ],
            [
              -79.54592349267301,
              43.71082804565404
            ],
            [
              -79.52373079738383,
              43.71598406529472
            ],
            [
              -79.51967596795846,
              43.71631496042619
            ],
            [
              -79.52360156656403,
              43.724206921002946
            ],
            [
              -79.52782011664385,
              43.742188417395795
            ],
            [
              -79.5335435207321,
              43.76620037707238
            ],
            [
              -79.53483113396182,
              43.77271081798696
            ],
            [
              -79.57487017078941,
              43.76433809556718
            ],
            [
              -79.57849582404157,
              43.7635230635002
            ],
            [
              -79.58163900633889,
              43.76107834909325
            ],
            [
              -79.58373475415604,
              43.76037969957042
            ],
            [
              -79.58534449026543,
              43.760147839730365
            ],
            [
              -79.58912871816703,
              43.759857720819866
            ],
            [
              -79.59097909092353,
              43.75939299935638
            ],
            [
              -79.59274929479011,
              43.75939343422294
            ],
            [
              -79.59532541397513,
              43.759626253067694
            ],
            [
              -79.61406299415567,
              43.755502175256055
            ],
            [
              -79.60900134020565,
              43.747364386576834
            ],
            [
              -79.60224788745066,
              43.73206633123124
            ],
            [
              -79.59567998794834,
              43.71737000250556
            ],
            [
              -79.58235668959941,
              43.71417890491537
            ],
            [
              -79.57598807484577,
              43.71265389561725
            ],
            [
              -79.57059089679503,
              43.71140741179144
            ],
            [
              -79.56883269026838,
              43.711379169925294
            ],
            [
              -79.56668377117961,
              43.71168982972239
            ],
            [
              -79.55463119685356,
              43.71442404640791
            ]
]
polygon = Polygon(boundary_coords)

# -------------------------------
# CACHED GEOCODING FUNCTION - For Nominatim compliance
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def cached_geocode_address(address, user_agent_string):
    """Cached geocoding function to comply with Nominatim caching policy."""
    
    # Create geolocator with the specific user agent
    geolocator = Nominatim(user_agent=user_agent_string, timeout=20)
    
    # Try geocoding with retries
    for attempt in range(3):
        try:
            location = geolocator.geocode(address)
            
            if location:
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'success': True,
                    'attempts': attempt + 1
                }
            else:
                # No location found
                return {
                    'latitude': None,
                    'longitude': None,
                    'success': False,
                    'attempts': attempt + 1,
                    'error': 'No location found'
                }
                
        except GeocoderTimedOut:
            if attempt < 2:  # Don't sleep on last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
        except GeocoderUnavailable:
            if attempt < 2:
                time.sleep(2 ** attempt)
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
    
    # All attempts failed
    return {
        'latitude': None,
        'longitude': None,
        'success': False,
        'attempts': 3,
        'error': 'All geocoding attempts failed'
    }

def is_address_in_boundary(address, user_agent, retries=3):
    """Check if the address is inside the defined polygon, with caching."""
    
    # Get cached geocoding result
    cache_result = cached_geocode_address(address, user_agent)
    
    if not cache_result['success']:
        # Geocoding failed
        debug_messages = [
            f"❌ Geocoding failed: {cache_result.get('error', 'Unknown error')}",
            f"📊 Attempts made: {cache_result['attempts']}"
        ]
        return False, None, debug_messages
    
    # Geocoding succeeded - check boundary
    lat = cache_result['latitude']
    lon = cache_result['longitude']
    
    debug_messages = [
        f"✅ Using cached result for: {address}",
        f"📍 Coordinates: {lat:.6f}, {lon:.6f}",
        f"📊 Geocoding attempts: {cache_result['attempts']}"
    ]
    
    # Check if point is inside polygon
    point = Point(lon, lat)
    is_inside = polygon.contains(point)
    
    debug_messages.append(f"🎯 Point inside boundary: {is_inside}")
    
    return is_inside, (lat, lon), debug_messages

def is_valid_email(email):
    """Check if email format is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# -------------------------------
# Streamlit UI
st.set_page_config(page_title="Ernestine's Address Checker", layout="centered")

# Header
st.markdown(
    """
    <div style="text-align: center; padding-bottom: 20px;">
        <h1 style="margin-bottom: 0;">Ernestine's Address Checker</h1>
        <p style="font-size:12px; margin-top:5px;">Created by J Sivec</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Email input for Nominatim user agent
st.subheader("📧 Required: Email for Geocoding Service")
email_input = st.text_input(
    "Enter your email address (required by OpenStreetMap's Nominatim service):",
    placeholder="your_email@example.com",
    help="This is required for the geocoding service. Your email is only used to comply with their terms of service."
)

# Address input
st.subheader("🏠 Address Check")

# Show example address format
st.info("""
**📝 Address Format Example:**
```
123 Main Street, Toronto, ON
2889 Islington Ave, North York, ON M9L 2T3
456 Queen Street West, Toronto, ON M5H 2N2
```

**Requirements:**
- Include street number and name
- Include city and province
- Postal code is optional but recommended
- Use "ON" for Ontario (not "Ont." or "Ontario")
- **⚠️ Exclude unit/apartment numbers** (e.g., don't use "123-456 Main St" or "123 Main St Unit 3" - just "123 Main St")
""")

address_input = st.text_input(
    "Enter the complete address to check:",
    placeholder="123 Main Street, Toronto, ON",
    help="Enter the full address including street, city, and province. The app will determine if it's inside the Etobicoke boundary."
)

# Check button and results
if st.button("Check Address", type="primary"):
    # Validate email format
    if not email_input:
        st.error("❌ Please enter your email address first (required for geocoding).")
    elif not is_valid_email(email_input):
        st.error("❌ Please enter a valid email address (e.g., user@example.com)")
    elif not address_input:
        st.warning("⚠ Please enter an address.")
    else:
        # Use proper user agent with user's email for Nominatim compliance
        user_agent = f"ernestines_address_checker/1.0 ({email_input})"
        st.info(f"🔧 Using user agent: `{user_agent}`")
        
        # Use the cached geocoding function
        with st.spinner("🔍 Geocoding address... This may take a few seconds."):
            inside, coords, debug_messages = is_address_in_boundary(address_input, user_agent)
        
        if coords is None:
            st.error("❌ Address could not be geocoded. See debug information below for details.")
            st.info("💡 **Tips:** Include the full address with street number, city, and province.")
        else:
            status = "INSIDE" if inside else "OUTSIDE"
            # REVERSED: Inside = Red, Outside = Green
            color = "🔴" if inside else "🟢"
            
            # BIG PROMINENT RESULT BOX - Right under the button
            st.markdown(f"""
            <div style="
                background-color: {'#f8d7da' if inside else '#d4edda'}; 
                border: 3px solid {'#dc3545' if inside else '#28a745'}; 
                border-radius: 15px; 
                padding: 30px; 
                margin: 20px 0; 
                text-align: center;
                font-size: 28px;
                color: {'#721c24' if inside else '#155724'};
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            ">
                {color} <strong>Result: {status}</strong> Boundary
            </div>
            """, unsafe_allow_html=True)
            
            # Additional details below the big result
            st.info(f"📍 **Coordinates:** {coords[0]:.6f}, {coords[1]:.6f}")
            st.info(f"🏠 **Address checked:** {address_input}")

# Information section
st.markdown("---")
st.subheader("ℹ️ How It Works")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔍 Geocoding Process:**
    - Converts your address to latitude/longitude coordinates
    - Uses OpenStreetMap's Nominatim service (free)
    - Checks if coordinates fall within the defined Etobicoke boundary
    
    **📊 Boundary:**
    - Covers a specific area of Etobicoke, Toronto
    - Boundary coordinates are predefined in the system
    - Cannot be modified by users
    """)

with col2:
    st.markdown("""
    **💡 Tips for Best Results:**
    - Include full address (street number, name, city)
    - Add postal code if possible
    - Check spelling carefully
    
    **⚠️ Common Issues:**
    - New addresses may not be in the geocoding database yet
    - Some rural addresses may not geocode accurately
    - Service may be temporarily unavailable
    """)

# Technical details
with st.expander("🔧 Technical Details"):
    st.markdown("""
    **Technology Stack:**
    - **Frontend:** Streamlit (Python web framework)
    - **Geocoding:** GeoPy with Nominatim (OpenStreetMap)
    - **Geometry:** Shapely (computational geometry)
    - **Mapping:** Uses predefined polygon coordinates
    
    **Data Sources & Licensing:**
    - **Geocoding Data:** Powered by OpenStreetMap's Nominatim service
    - **License Compliance:** Follows OpenStreetMap's usage policy and ODbL requirements
    - **Attribution:** Map data © OpenStreetMap contributors, available under ODbL
    - **Service Switchability:** Can switch geocoding providers if required
    
    **Rate Limits:**
    - Nominatim allows limited requests per user
    - Email helps prevent abuse and manage fair usage
    - Automatic retries with exponential backoff
    
    **Privacy:**
    - Email is only used for Nominatim compliance
    - Address lookups are sent to OpenStreetMap's Nominatim service for geocoding
    - Boundary checking is processed locally using coordinates
    - No data is stored locally or shared with third parties
    """)

# Footer with proper ODbL attribution
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 11px; line-height: 1.4; background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <p style="margin-bottom: 8px;"><strong>Geocoding Service</strong></p>
        <p style="margin-bottom: 8px;">
            <a href="https://www.openstreetmap.org/copyright" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">
                Map data from OpenStreetMap
            </a>
        </p>
        <p style="margin-bottom: 8px; font-style: italic;">
            This data is available under the 
            <a href="https://opendatacommons.org/licenses/odbl/" target="_blank" style="color: #007bff; text-decoration: none;">
                Open Database License
            </a>
        </p>
        <p style="margin-bottom: 8px; font-size: 10px;">© OpenStreetMap contributors</p>
        <p style="margin-bottom: 0; font-size: 10px;">Built with ❤️ using Streamlit, GeoPy, and Shapely</p>
    </div>
    """,
    unsafe_allow_html=True
)

