import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, redirect
from glide_sdk import GlideClient
import asyncio
from functools import wraps

# Helper function to run async code in sync Flask routes
def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

app = Flask(__name__, 
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    static_url_path=''
)

# Global variables to store session data
session_data = {}
current_session_data = None

# Initialize Glide client
glide_client = GlideClient()

# Configuration
PORT = int(os.getenv('PORT', 4568))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/getAuthUrl')
@async_route
async def get_auth_url():
    """Generate authentication URL for phone verification"""
    try:
        phone_number = request.args.get('phoneNumber')
        state = str(uuid.uuid4())
        
        auth_url = await glide_client.number_verify.get_auth_url(
            state=state,
            use_dev_number=phone_number
        )
        
        session_data[state] = {
            'phoneNumber': phone_number,
            'authUrl': auth_url
        }
        
        return jsonify({'authUrl': auth_url})
    
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/api/getSessionData')
def get_session_data():
    """Retrieve current session data"""
    try:
        global session_data, current_session_data
        
        if not current_session_data:
            return jsonify({})
        
        response = jsonify(current_session_data)
        
        # Clear session data after sending
        session_data = {}
        current_session_data = None
        
        return response
    
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/callback')
def callback():
    """Handle the callback from phone verification"""
    try:
        global current_session_data
        
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if state not in session_data:
            session_data[state] = {
                'error': 'No session data found for state'
            }
            print(f'No session data found for state {state}')
            return redirect('/')
        
        session_data[state]['code'] = code
        if error:
            error_description = request.args.get('error_description')
            session_data[state]['error'] = error_description
        
        current_session_data = session_data[state]
        return send_from_directory('static', 'index.html')
    
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/api/verifyNumber', methods=['POST'])
@async_route
async def verify_number():
    """Verify the phone number"""
    try:
        data = request.get_json()
        code = data.get('code')
        phone_number = data.get('phoneNumber')
        
        user_client = await glide_client.number_verify.for_user(
            code=code,
            phone_number=phone_number
        )
        
        operator = await user_client.get_operator()
        verify_res = await user_client.verify_number()
        
        return jsonify({
            'operator': operator,
            'verifyRes': {
                'devicePhoneNumberVerified': verify_res.devicePhoneNumberVerified,
            }
        })
    
    except Exception as error:
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    # For development, use debug=True
    app.run(host='0.0.0.0', port=PORT, debug=True)
