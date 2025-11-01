import geocoder

def get_current_location():
    """Get the current location using IP address"""
    try:
        g = geocoder.ip('me')
        if g.ok:
            # Return city and state/region
            location_parts = []
            if g.city:
                location_parts.append(g.city)
            if g.state:
                location_parts.append(g.state)
            return ", ".join(location_parts) if location_parts else "Unknown"
        return "Unknown"
    except Exception:
        return "Unknown"