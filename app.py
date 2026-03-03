# import os
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# import json
# from flask import Flask, render_template, request, redirect, url_for
# from openai import OpenAI
# from dotenv import load_dotenv
# from flask import flash
# from flask_mail import Mail, Message

# from flask_login import login_required
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
# from flask_dance.contrib.google import make_google_blueprint, google
# from flask_dance.consumer import oauth_authorized
# from werkzeug.security import generate_password_hash, check_password_hash

 
# load_dotenv()

# app = Flask(__name__)
# from werkzeug.middleware.proxy_fix import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
# app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev_key_123_local')

 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# with app.app_context():
#     print("Checking/Creating database tables...")
#     db.create_all()   
#     print("✅ Database tables are ready!")
#     db.create_all()
 
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     google_id = db.Column(db.String(100), unique=True, nullable=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     password_hash = db.Column(db.String(200), nullable=True)
    
#     profile_picture = db.Column(db.String(500), nullable=True)

#     income = db.Column(db.Integer)
#     category = db.Column(db.String(50))  
#     state = db.Column(db.String(100))
#     education = db.Column(db.String(100))
#     gender = db.Column(db.String(20))
#     profile_complete = db.Column(db.Boolean, default=False)
#     last_notified_scheme_count = db.Column(db.Integer, default=0)

# class Scholarship(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    
#     scheme_name = db.Column(db.String(255), nullable=False)
#     link = db.Column(db.String(500), unique=True, nullable=False)
#     description = db.Column(db.Text)
#     eligibility_criteria = db.Column(db.Text)   
#     benefits = db.Column(db.Text)
#     required_documents = db.Column(db.Text)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)

 
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'google.login'

# @login_manager.user_loader
# def load_user(user_id):
  
#     return db.session.get(User, int(user_id))

 
# client = OpenAI(
#   base_url = "https://integrate.api.nvidia.com/v1",
#   api_key = os.getenv("NVIDIA_API_KEY")
# )

# blueprint = make_google_blueprint(
#     client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
     
#     scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
#     offline=True,
# )
# app.register_blueprint(blueprint, url_prefix="/login")

 
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form.get('full_name')
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         user_exists = User.query.filter_by(email=email).first()
#         if user_exists:
            
#             return redirect(url_for('login'))
        
         
#         new_user = User(
#             name=name, 
#             email=email, 
#             password_hash=generate_password_hash(password)
#         )
#         db.session.add(new_user)
#         db.session.commit()
        
        
        
#         return redirect(url_for('login'))  
    
#     return render_template('signup.html')



 
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         user = User.query.filter_by(email=email).first()
        
#         if user and check_password_hash(user.password_hash, password):
#             login_user(user)
            
#             if not user.profile_complete:
#                 return redirect(url_for('profile'))
#             return redirect(url_for('dashboard'))
#         else:
#             flash("Invalid credentials!")
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     logout_user()
    
#     return redirect(url_for('index'))

 



# @app.route('/')
# def index():
    
#     return render_template('home.html')



# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
# app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
 
# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
# mail = Mail(app)



# def send_match_email(user_email, user_name, match_details):
#     print(f"Attempting to send mail to: {user_email}...")
    
     
#     my_email = os.getenv("MAIL_USERNAME")
    
   
#     msg = Message(
#         subject='ScholarAI: Your Matched Scholarships Are Here! 🎓',
#         recipients=[user_email],
#         sender=my_email,   
#         body=f"Hi {user_name},\n\nBased on your profile, our AI found the following matches:\n\n{match_details}\n\nBest of luck!\nTeam ScholarAI"
#     )
    
#     try:
         
#         with app.app_context():
#             mail.send(msg)
#         print("✅ SUCCESS: Email has been sent!")
#     except Exception as e:
#         print(f"❌ Email error: {str(e)}")


# @app.route('/dashboard')
# @login_required
# def dashboard():
     
#     all_schemes = Scholarship.query.all()
    
#     schemes_text = ""
#     for s in all_schemes:
#         schemes_text += f"Name: {s.scheme_name},ID:{s.id}, Eligibility: {s.eligibility_criteria}, Link: {s.link}\n"

#     prompt = f"""
#     You are a Scholarship Matchmaker.
#     Database Schemes: {schemes_text}
#     User Profile: Category: {current_user.category}, State: {current_user.state}
#     AVAILABLE SCHEMES:
#     {schemes_text}
#     STRICT RULES:
#     1. Only return schemes that match the user's category ({current_user.category}). If a scheme is for another category, IGNORE IT.
#     2. Only return schemes for the user's state ({current_user.state}) or National level.
#     3. Use the exact 'Link' provided in the data.
#     4. Return exactly 8-10 best matches in JSON format.

#     JSON Structure:
#     [
#       {{
#         "name": "Scheme Name",
#         "eligibility": "Brief eligibility",
#         "benefits": "Brief benefits",
#         "link": "Actual URL",
#         "match_score": "95%",
#         "deadline": "April 2026"
#       }}
#     ]
#     Task: Return a JSON list of matched schemes. 
#     CRITICAL: You MUST use the exact 'link' provided in the Database Schemes.
#     Format: [{{"name": "...", "eligibility": "...", "benefits": "...", "link": "URL", "match_score": "95%", "deadline": "Mar 30"}}]
#     """

    

#     try:
#         completion = client.chat.completions.create(
#             model="meta/llama-3.1-8b-instruct",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.1,
            
#         )
        
#         raw_response = completion.choices[0].message.content
#         clean_json = raw_response.replace("```json", "").replace("```", "").strip()
#         schemes_list = json.loads(clean_json)
        
#     except Exception as e:
#         print(f"AI Error: {e}")
#         schemes_list = []
#         for s in all_schemes[:8]:
#             schemes_list.append({
#                 "name": s.scheme_name,
#                 "eligibility": s.eligibility_criteria,
#                 "benefits": "Check link for details",
#                 "link": s.link,
#                 "match_score": "90%",
#                 "deadline": "May 2026"
#             })

  
#     current_total_schemes = len(schemes_list)

#     if current_total_schemes > current_user.last_notified_scheme_count:

#         match_details = ""

#         for scheme in schemes_list:
#             match_details += f"""
# Name: {scheme['name']}
# Match Score: {scheme['match_score']}
# Deadline: {scheme['deadline']}
# Apply Link: {scheme['link']}

# """

#         send_match_email(current_user.email, current_user.name, match_details)

#         current_user.last_notified_scheme_count = current_total_schemes
#         db.session.commit()

#     return render_template('dashboard.html', schemes_list=schemes_list)




# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html')


# @app.route('/save_profile', methods=['POST'])
# @login_required
# def save_profile():
    
#     current_user.name = request.form.get('full_name')  
#     current_user.income = int(request.form.get('income'))
#     current_user.category = request.form.get('category')
#     current_user.state = request.form.get('state')
#     current_user.education = request.form.get('education')
#     current_user.gender = request.form.get('gender')
    
  
    
#     current_user.profile_complete = True
#     db.session.commit()
#     return redirect(url_for('dashboard'))


# @app.route('/get_scholarship', methods=['POST'])
# def get_scholarship():
#     user_query = request.form.get('query')
#     completion = client.chat.completions.create(
#       model="meta/llama-3.1-8b-instruct",
#       messages=[{"role": "user", "content": f"Find Indian government scholarships for: {user_query}"}],
#       temperature=0.2,
#       max_tokens=1024,
#     )
#     ai_response = completion.choices[0].message.content
#     return render_template('index.html', result=ai_response)

 

# @oauth_authorized.connect_via(blueprint)
# def google_logged_in(blueprint, token):
#     resp = google.get("/oauth2/v1/userinfo")
#     if resp.ok:
#         info = resp.json()
#         email = info["email"]
#         google_id = str(info["id"])
#         picture = info.get("picture")   

#         user = User.query.filter_by(google_id=google_id).first()

#         if not user:
#             user = User.query.filter_by(email=email).first()

#             if user:
#                 user.google_id = google_id
#                 user.profile_picture = picture
#             else:
#                 user = User(
#                     google_id=google_id,
#                     name=info["name"],
#                     email=email,
#                     profile_picture=picture 
#                 )
#                 db.session.add(user)
#         else:
#             user.profile_picture = picture   

#         db.session.commit()
#         login_user(user)

#         if not user.profile_complete:
#             return redirect(url_for('profile'))
#         return redirect(url_for('dashboard'))
#     return False





# @app.route('/test_mail')
# def test_mail():
#     try:
#         msg = Message('Testing ScholarAI',
#                       sender=app.config['MAIL_USERNAME'],
                      
#                       recipients=[current_user.email])
#         msg.body = "mail !"
#         mail.send(msg)
#         return "✅ Mail Sent Successfully! Check your inbox."
#     except Exception as e:
#         return f"❌ Mail Failed: {str(e)}"

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import json
from datetime import datetime

# Environment setup
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from openai import OpenAI

app = Flask(__name__)

# 1. FIX: ProxyFix is required for Render to handle HTTPS correctly
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev_key_123_local')

# 2. FIX: Database configuration
# Note: On Render, SQLite data will disappear on restart. 
# Consider using Render PostgreSQL for a permanent database.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200), nullable=True)
    profile_picture = db.Column(db.String(500), nullable=True)
    income = db.Column(db.Integer)
    category = db.Column(db.String(50))  
    state = db.Column(db.String(100))
    education = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    profile_complete = db.Column(db.Boolean, default=False)
    last_notified_scheme_count = db.Column(db.Integer, default=0)

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(500), unique=True, nullable=False)
    description = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text)   
    benefits = db.Column(db.Text)
    required_documents = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# 3. FIX: Enhanced Table Creation
with app.app_context():
    print("Checking/Creating database tables...")
    db.create_all()   
    print("✅ Database tables are ready!")

# --- Auth Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_API_KEY")
)

blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
    offline=True,
)
app.register_blueprint(blueprint, url_prefix="/login")

# --- Routes ---

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash("Email already exists. Please login.")
            return redirect(url_for('login'))
        
        new_user = User(
            name=name, 
            email=email, 
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if not user.profile_complete:
                return redirect(url_for('profile'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- Email Setup ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

def send_match_email(user_email, user_name, match_details):
    msg = Message(
        subject='ScholarAI: Your Matched Scholarships Are Here! 🎓',
        recipients=[user_email],
        body=f"Hi {user_name},\n\nBased on your profile, our AI found matches:\n\n{match_details}\n\nBest of luck!"
    )
    try:
        with app.app_context():
            mail.send(msg)
        print("✅ SUCCESS: Email sent!")
    except Exception as e:
        print(f"❌ Email error: {str(e)}")

# --- Dashboard & AI ---

@app.route('/dashboard')
@login_required
def dashboard():
    all_schemes = Scholarship.query.all()
    schemes_text = "".join([f"Name: {s.scheme_name}, Eligibility: {s.eligibility_criteria}, Link: {s.link}\n" for s in all_schemes])

    prompt = f"Match scholarships for: Category: {current_user.category}, State: {current_user.state}. Data: {schemes_text}. Return JSON list."

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        raw_response = completion.choices[0].message.content
        clean_json = raw_response.replace("```json", "").replace("```", "").strip()
        schemes_list = json.loads(clean_json)
    except Exception as e:
        print(f"AI Error: {e}")
        schemes_list = [] # Fallback logic can go here

    # Email notification logic
    if len(schemes_list) > current_user.last_notified_scheme_count:
        details = "\n".join([f"{s['name']}: {s['link']}" for s in schemes_list])
        send_match_email(current_user.email, current_user.name, details)
        current_user.last_notified_scheme_count = len(schemes_list)
        db.session.commit()

    return render_template('dashboard.html', schemes_list=schemes_list)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/save_profile', methods=['POST'])
@login_required
def save_profile():
    current_user.name = request.form.get('full_name')  
    current_user.income = int(request.form.get('income') or 0)
    current_user.category = request.form.get('category')
    current_user.state = request.form.get('state')
    current_user.education = request.form.get('education')
    current_user.gender = request.form.get('gender')
    current_user.profile_complete = True
    db.session.commit()
    return redirect(url_for('dashboard'))

# --- OAuth Authorization Handling ---

@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        return False

    info = resp.json()
    email = info["email"]
    google_id = str(info["id"])
    picture = info.get("picture")

    # 4. FIX: Robust user lookup and creation
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User.query.filter_by(email=email).first()
        if user:
            user.google_id = google_id
        else:
            user = User(google_id=google_id, name=info["name"], email=email)
            db.session.add(user)
    
    user.profile_picture = picture
    db.session.commit()
    login_user(user)

    # 5. FIX: Return the redirect directly
    if not user.profile_complete:
        return redirect(url_for('profile'))
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)