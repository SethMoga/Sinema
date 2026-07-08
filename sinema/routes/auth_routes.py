from flask import Blueprint, request, jsonify, render_template, redirect
from services.auth_service import login_auth
from services.auth_service import logout_auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    print('WELCOME TO LOGIN!')

    if request.method == 'POST':
        # POST request handling
        data = request.form
        #   print(data)
        
        #create local vars
        username = data.get("username")
        password = data.get("password")
        print("username:", username)
        print("password:", password)
        
        #call service function
        result = login_auth(username, password)
        print(result)
        #   return jsonify(result)
        return redirect('/')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout_route():
    #call service function
    result = logout_auth()
    print(result)
    #   return jsonify(result)
    return redirect('/')