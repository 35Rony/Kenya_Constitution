from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini API
# Set your API key as an environment variable: export GEMINI_API_KEY='your-api-key'
GEMINI_API_KEY = os.environ.get('AIzaSyDC7HmuZDIWXI2hD-XsxTskKa_IN7jZeyE', '')

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not set. Please set it as an environment variable.")
    print("Get your API key from: https://makersuite.google.com/app/apikey")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# The complete Kenyan Constitution text (loaded from your PDF)
CONSTITUTION_TEXT = """
LAWS OF KENYA
THE CONSTITUTION OF KENYA, 2010

PREAMBLE
We, the people of Kenya—
ACKNOWLEDGING the supremacy of the Almighty God of all creation:
HONOURING those who heroically struggled to bring freedom and justice to our land:
PROUD of our ethnic, cultural and religious diversity, and determined to live in peace and unity as one indivisible sovereign nation:
RESPECTFUL of the environment, which is our heritage, and determined to sustain it for the benefit of future generations:
COMMITTED to nurturing and protecting the well-being of the individual, the family, communities and the nation:
RECOGNISING the aspirations of all Kenyans for a government based on the essential values of human rights, equality, freedom, democracy, social justice and the rule of law:
EXERCISING our sovereign and inalienable right to determine the form of governance of our country and having participated fully in the making of this Constitution:
ADOPT, ENACT and give this Constitution to ourselves and to our future generations.

CHAPTER ONE—SOVEREIGNTY OF THE PEOPLE AND SUPREMACY OF THIS CONSTITUTION

Article 1 - Sovereignty of the people
(1) All sovereign power belongs to the people of Kenya and shall be exercised only in accordance with this Constitution.
(2) The people may exercise their sovereign power either directly or through their democratically elected representatives.
(3) Sovereign power under this Constitution is delegated to Parliament, the national executive and county executives, and the Judiciary.

Article 2 - Supremacy of this Constitution
(1) This Constitution is the supreme law of the Republic and binds all persons and all State organs at both levels of government.
(2) No person may claim or exercise State authority except as authorised under this Constitution.
(3) The validity or legality of this Constitution is not subject to challenge by or before any court or other State organ.
(4) Any law, including customary law, that is inconsistent with this Constitution is void to the extent of the inconsistency.

Article 3 - Defence of this Constitution
(1) Every person has an obligation to respect, uphold and defend this Constitution.
(2) Any attempt to establish a government otherwise than in compliance with this Constitution is unlawful.

CHAPTER TWO—THE REPUBLIC

Article 4 - Declaration of the Republic
(1) Kenya is a sovereign Republic.
(2) The Republic of Kenya shall be a multi-party democratic State founded on the national values and principles of governance referred to in Article 10.

Article 10 - National values and principles of governance
The national values and principles of governance include:
(a) patriotism, national unity, sharing and devolution of power, the rule of law, democracy and participation of the people;
(b) human dignity, equity, social justice, inclusiveness, equality, human rights, non-discrimination and protection of the marginalised;
(c) good governance, integrity, transparency and accountability;
(d) sustainable development.

CHAPTER FOUR—THE BILL OF RIGHTS

Article 19 - Rights and fundamental freedoms
The Bill of Rights is an integral part of Kenya's democratic state and is the framework for social, economic and cultural policies.

Article 27 - Equality and freedom from discrimination
Every person is equal before the law and has the right to equal protection and equal benefit of the law. The State shall not discriminate on grounds including race, sex, pregnancy, marital status, health status, ethnic or social origin, colour, age, disability, religion, conscience, belief, culture, dress, language or birth.

Article 43 - Economic and social rights
Every person has the right to:
(a) the highest attainable standard of health, including reproductive health care;
(b) accessible and adequate housing, and reasonable standards of sanitation;
(c) to be free from hunger, and to have adequate food of acceptable quality;
(d) clean and safe water in adequate quantities;
(e) social security;
(f) education.

Article 47 - Fair administrative action
Every person has the right to administrative action that is expeditious, efficient, lawful, reasonable and procedurally fair.

CHAPTER SIX—LEADERSHIP AND INTEGRITY

Article 73 - Responsibilities of leadership
Authority assigned to a State officer is a public trust to be exercised in a manner that demonstrates respect for the people, brings honour to the nation, and promotes public confidence in the integrity of the office.

CHAPTER ELEVEN—DEVOLVED GOVERNMENT

Article 174 - Objects of devolution
The objects of devolution include:
(a) promoting democratic and accountable exercise of power;
(b) fostering national unity by recognising diversity;
(c) giving powers of self-governance to the people;
(d) protecting and promoting interests of minorities and marginalised communities;
(e) promoting social and economic development;
(f) ensuring equitable sharing of national and local resources.

Article 176 - County governments
There shall be a county government for each of the 47 counties, consisting of a county assembly and a county executive.

CHAPTER TWELVE—PUBLIC FINANCE

Article 201 - Principles of public finance
Public finance shall be guided by:
(a) openness and accountability, including public participation;
(b) equitable sharing of revenue between national and county governments;
(c) prudent and responsible use of public money;
(d) clear fiscal reporting.

[Note: This is a condensed version. The full constitution contains 264 articles across 18 chapters with detailed provisions on citizenship, land, environment, legislature, executive, judiciary, national security, commissions, and amendments.]
"""

def query_gemini(user_question):
    """
    Query Gemini API with the constitution context and user question
    """
    try:
        prompt = f"""You are a helpful assistant that answers questions about the Kenyan Constitution of 2010. 
        
Use the following constitution text to answer the user's question accurately and comprehensively:

{CONSTITUTION_TEXT}

User Question: {user_question}

Instructions:
1. Answer based ONLY on the information provided in the constitution text above
2. If the constitution text doesn't contain enough information to answer fully, say so
3. Cite specific articles when relevant
4. Be clear, accurate, and helpful
5. If asked about specific articles, provide the full text and explanation
6. Keep your response concise but complete (2-4 paragraphs maximum)

Answer:"""

        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error querying Gemini: {str(e)}"

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint that receives questions and returns AI-generated answers
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400
        
        # Check if API key is configured
        if not GEMINI_API_KEY:
            return jsonify({
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY environment variable.'
            }), 500
        
        # Query Gemini with the constitution context
        ai_response = query_gemini(user_message)
        
        return jsonify({
            'response': ai_response,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    api_configured = bool(GEMINI_API_KEY)
    return jsonify({
        'status': 'healthy',
        'gemini_configured': api_configured,
        'message': 'Gemini API is configured' if api_configured else 'Gemini API key not set'
    })

@app.route('/', methods=['GET'])
def home():
    """
    Home route with API information
    """
    return jsonify({
        'app': 'Kenyan Constitution Chatbot',
        'version': '2.0',
        'powered_by': 'Google Gemini AI',
        'endpoints': {
            'chat': '/api/chat (POST)',
            'health': '/api/health (GET)'
        },
        'setup_instructions': 'Set GEMINI_API_KEY environment variable with your API key from https://makersuite.google.com/app/apikey'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Kenyan Constitution Chatbot - Gemini Powered")
    print("=" * 60)
    if GEMINI_API_KEY:
        print("✓ Gemini API Key: Configured")
    else:
        print("✗ Gemini API Key: NOT CONFIGURED")
        print("\nTo set up:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print("3. Restart the server")
    print("=" * 60)
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)