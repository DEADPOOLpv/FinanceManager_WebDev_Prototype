from flask import Blueprint, request, render_template, jsonify, session, current_app
from .database import insert_expense
from llama_cpp import Llama
from .models import User
from flask import current_app, redirect, url_for

from .models import CategoryExpenses,Expenses

main = Blueprint('main', __name__)

# Load the model once globally
llm = Llama.from_pretrained(
    repo_id="nguyentd/FinancialAdvice-Qwen2.5-7B.gguf",
    filename="FinancialAdvice-Qwen2.5-7B.Q8_0.gguf"
)
#routes to files in the templates folder
@main.route('/')
def home():
    print("Template Path:", current_app.template_folder)
    return render_template('home.html')

@main.route('/category')
def category():
    print("Template Path:", current_app.template_folder)
    return render_template('category.html')

@main.route('/graph')
def graph():  
    print("Template Path:", current_app.template_folder)
    return render_template('garph.html')

@main.route('/graph2')
def graph2():  
    print("Template Path:", current_app.template_folder)
    return render_template('graph2.html')

@main.route('/basic recommendation')
def basic_recommendation():  
    print("Template Path:", current_app.template_folder)
    return render_template('basic recommendation.html')

@main.route('/ai recommendation')
def ai_recommendation():  
    print("Template Path:", current_app.template_folder)
    return render_template('ai reccomendation.html')



@main.route('/display')
def display():  
    print("Template Path:", current_app.template_folder)
    return render_template('display.html')

@main.route('/homepage')
def homepage():
    print("Template Path:", current_app.template_folder)
    return render_template('homepage.html')

@main.route('/login')
def login():
    print("Template Path:", current_app.template_folder)
    return render_template('login.html')

@main.route('/add')
def add():
    print("Template Path:", current_app.template_folder)
    return render_template('add.html')

@main.route('/today')
def today():
    print("Template Path:", current_app.template_folder)
    return render_template('today.html')

@main.route('/month')
def month():
    print("Template Path:", current_app.template_folder)
    return render_template('month.html')

@main.route('/year')
def year():
    print("Template Path:", current_app.template_folder)
    return render_template('year.html')


#routes for  AI(basic recommendation)
@main.route('/get_basic_recommendations', methods=['POST'])
def get_basic_recommendations():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input data"}), 400

        # Extract total expenditure and salary
        total_expenditure = data.get('totalExpenditure')
        salary = data.get('salary')

        # Ensure both fields are provided
        if total_expenditure is None or salary is None:
            return jsonify({"error": "Total expenditure and salary are required fields"}), 400

        # Calculate expense percentage
        expense_percentage = round((total_expenditure / salary) * 100, 2)

        # Construct a simplified message for the AI model
        user_message = f"""
        My total monthly expenditure is ₹{total_expenditure}, which is {expense_percentage}% of my monthly income of ₹{salary}.
        Based on this data:
        1. Assess whether this spending level is reasonable.
        2. Provide actionable financial advice for optimizing savings and discretionary spending.
        3. Ensure the advice is:
        - Focused only on local, day-to-day financial management.
        - Relevant to the Indian context.
        - Free of investment suggestions or global financial comparisons.

        Respond in a concise, professional, and respectful manner. Use the Indian Rupee symbol (₹) in your response.
        """

        # Send the request to the AI model
        response = llm.create_chat_completion(
            messages=[{"role": "user", "content": user_message}],
            max_tokens=200
        )
        raw_recommendations = response['choices'][0]['message']['content']

        # Refine the AI's response to remove unnecessary or inconsistent content
        refined_recommendations = refine_ai_response(raw_recommendations)

        return jsonify({"recommendations": refined_recommendations}), 200

    except Exception as e:
        print(f"Error in get_basic_recommendations: {e}")
        return jsonify({"error": "An error occurred while processing the request"}), 500
    #Fine tuning the AI model
def refine_ai_response(response):
    """
    Cleans up the AI's response to ensure consistency and remove unnecessary or irrelevant content.
    """
    # Define key phrases to look for and remove if present
    disallowed_phrases = [
        "The average Indian",  
        "If you are retired",
        "S&P 500",  
        "ETFs",     
        "US market",
    ]

    # Break response into sentences
    sentences = response.split(". ")
    refined_sentences = []

    for sentence in sentences:
        # Skip sentences with disallowed phrases
        if any(phrase in sentence for phrase in disallowed_phrases):
            continue
        refined_sentences.append(sentence)

    # Join the refined sentences back
    refined_response = ". ".join(refined_sentences).strip()
    
    # Ensure proper punctuation
    if not refined_response.endswith("."):
        refined_response += "."

    return refined_response

    

#routes for AI(ai recommendation)
@main.route('/get_financial_advice', methods=['POST'])
def get_financial_advice():
    try:
        # Parse the JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input data"}), 400

        # Extract required fields
        salary = data.get('salary')

        # Extract optional category-specific expenses (default to 0 if not provided)
        expenses = {
            "food": data.get('food', 0),
            "entertainment": data.get('entertainment', 0),
            "savings": data.get('savings', 0),
            "debt": data.get('debt', 0),
        }
        


        # Validate required fields
        if  salary is None:
            return jsonify({"error": "salary are required fields"}), 400

        # Validate numeric inputs
        try:
            salary = float(salary)
            expenses = {key: float(value) for key, value in expenses.items()}
            
        except ValueError:
            return jsonify({"error": "Expenses and salary must be numeric values"}), 400
    
        ideal_budget = {
            "food": round(salary * 0.30, 2),  # 30% of income for food
            "entertainment": round(salary * 0.10, 2),  # 10% for entertainment
            "savings": round(salary * 0.20, 2),  # 20% for savings
            "debt": round(salary * 0.15, 2),  # 15% for debt
        }

        # Construct the AI prompt
        user_message = f"""
        My monthly salary is ₹{salary}.
        My detailed monthly expenditures are:
        - Food: ₹{expenses['food']}
        - Entertainment: ₹{expenses['entertainment']}
        - Savings: ₹{expenses['savings']}
        - Debt: ₹{expenses['debt']}

        Based on my income, here are the ideal budget suggestions:
        - Ideal Food Budget: ₹{ideal_budget['food']}
        - Ideal Entertainment Budget: ₹{ideal_budget['entertainment']}
        - Ideal Savings: ₹{ideal_budget['savings']}
        - Ideal Debt Payment: ₹{ideal_budget['debt']}

        Please analyze my financial situation and provide:
        1. A clear and concise assessment of whether my spending is reasonable based on the provided data.
        2. Actionable advice to optimize my finances, including:
           - Suggestions for adjusting specific categories.
           - Recommended proportions for fixed and variable expenses, savings, and investments.

        Ensure:
        - Your response does not assume anything about my lifestyle,future plans and job.
        - Do not assume anything.
        - Advice is practical, relevant, and does not include judgments based on my current financial situation.
        - Use the Indian Rupee symbol (₹) consistently.
        """

        # Send the prompt to the AI model
        response = llm.create_chat_completion(
            messages=[{"role": "user", "content": user_message}]
        )

        # Extract and refine AI response
        raw_advice = response['choices'][0]['message']['content']
        refined_advice = refine_ai_response(raw_advice)

        return jsonify({"advice": refined_advice}), 200

    except Exception as e:
        # Log the exception for debugging
        print(f"Error in /get_financial_advice: {str(e)}")
        return jsonify({"error": f"Error retrieving financial advice: {str(e)}"}), 500


def refine_ai_response(response):
    """
    Refines the AI response to ensure it is neutral and avoids assumptions.
    """
    if not response:
        return "No advice could be generated. Please verify your input data."

    # Avoid assumptions about the user's future plans or lifestyle
    response = response.replace(
        "assuming you're young and just starting out",
        "without assuming anything about your background or circumstances."
    )

    response = response.replace(
        "if you're retired",
        "without making assumptions about your current stage in life."
    )

    # Avoid making assumptions about income sources
    response = response.replace(
        "if you have a steady income",
        "without assuming the nature of your income or employment."
    )

    # Add a polite tone where necessary
    if "doesn't make any sense" in response:
        response = response.replace(
            "doesn't make any sense",
            "might need clarification to provide better insights."
        )

    # Tailor advice to be actionable and region-specific without making assumptions
    if "50% rule" in response:
        response += " In India, adjusting this to fit local expenses may involve allocating more for rent and less for discretionary spending, depending on your city."

    if "apps like Swiftyexpense or SplitIt" in response:
        response += " Alternatively, you could use popular Indian apps like MoneyView or Walnut for tracking expenses."

    return response



#route for add.html adding expense
@main.route('/add_expense', methods=['POST'])
def add_expense():
    from app import mysql  # Import inside the function to avoid circular import issues
    data = request.get_json()
    amount = data.get('amount')
    salary = data.get('salary')
    date = data.get('date')
    
    # Retrieve user_id from session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

    if not amount or not salary or not date:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO expenses (user_id, amount, salary, date)
            VALUES (%s, %s, %s, %s)
        """, (user_id, amount, salary, date))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"status": "success", "message": "Expense added successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"}), 500
    
#route for category.html adding expenses
@main.route('/add_category_expense', methods=['POST'])
def add_category_expense():
    print(f"Session User ID: {session.get('user_id')}")
    from app import mysql
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        data = request.get_json()
        category_name = data.get('category')
        amount = data.get('amount')

        if not category_name or amount is None:
            return jsonify({"error": "Category and amount are required"}), 400

        cursor = mysql.connection.cursor()

        # Check if an entry already exists for this user and category
        cursor.execute(
            "SELECT amount FROM categories WHERE user_id = %s AND category_name = %s",
            (user_id, category_name)
        )
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Update the existing entry by adding the new amount to the current amount
            cursor.execute(
                "UPDATE categories SET amount = amount + %s WHERE user_id = %s AND category_name = %s",
                (amount, user_id, category_name)
            )
        else:
            # Insert a new entry with user_id, category_name, and amount
            cursor.execute(
                "INSERT INTO categories (user_id, category_name, amount) VALUES (%s, %s, %s)",
                (user_id, category_name, amount)
            )

        mysql.connection.commit()
        cursor.close()

        return jsonify({"status": "success", "message": "Category expense added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#route for signup
@main.route('/signup', methods=['POST'], endpoint="signup")
def signup():
    from app import db
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the username or email already exists
    existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
    if existing_user:
        return jsonify(message="Username or email already taken"), 409

    # Create a new user
    new_user = User(name=name, email=email)
    new_user.set_password(password)  # Hashes the password

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="Account created successfully"), 201
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify(message="Signup failed"), 500
#route for login
@main.route('/login', methods=['POST'], endpoint="login_endpoint")
def login():
    data = request.get_json()
    name = data.get('username')
    password = data.get('password')

    # Find user by username
    user = User.query.filter_by(name=name).first()
    if user and user.check_password(password):  # Assuming you have password check logic
        session['user_id'] = user.user_id  # Set the session variable
        session.permanent = True
    
    # Check if user exists and password matches
    if user and user.check_password(password):
        return jsonify(message="Login successful"), 200
    else:
        return jsonify(message="Invalid username or password"), 401
#route for logout
@main.route('/logout', methods=['GET'])
def logout():
    # Clear the user session
    session.clear()
   

#route for retrieving category expenses only
@main.route('/get_financial_data', methods=['GET'])
def get_financial_data():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        # Fetch only category-specific expenses (food, entertainment, savings, debt)
        category_expenses = CategoryExpenses.query.filter_by(user_id=user_id).all()
        # Create a dictionary for category expenses
        category_expenses_dict = {
            "food": 0,
            "entertainment": 0,
            "savings": 0,
            "debt": 0
        }

        for expense in category_expenses:
            if expense.category_name.lower() in category_expenses_dict:
                category_expenses_dict[expense.category_name.lower()] += expense.amount

        return jsonify({"categoryExpenses": category_expenses_dict}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#route for retrieving all expenses
@main.route('/get_display_data', methods=['GET'])
def get_display_data():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        # Fetch category expenses and initialize with predefined categories
        category_expenses = CategoryExpenses.query.filter_by(user_id=user_id).all()
        category_expenses_dict = {
            "food": 0,
            "entertainment": 0,
            "savings": 0,
            "debt": 0
        }

        # Summing up each category amount
        for expense in category_expenses:
            category = expense.category_name.lower()
            if category in category_expenses_dict:
                category_expenses_dict[category] += float(expense.amount)

        # Calculate the total expenditure amount
        total_general_expenses = sum(exp.amount for exp in Expenses.query.filter_by(user_id=user_id).all())
        
        # Fetch only the salary values for the specific user and get the maximum salary
        salary_entries = Expenses.query.filter_by(user_id=user_id).filter(Expenses.salary.isnot(None)).all()
        salary = max((exp.salary for exp in salary_entries), default=0)  # Simpler and clear


        return jsonify({
            "categoryExpenses": category_expenses_dict,
            "generalExpenses": total_general_expenses,
            "salary": salary
        }), 200

    except Exception as e:
        print("Error in get_display_data:", str(e))
        return jsonify({"error": "An error occurred while fetching data"}), 500
