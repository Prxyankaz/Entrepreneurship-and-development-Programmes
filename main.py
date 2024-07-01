from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

global p_id
p_id=25
# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Priyanka1710",
    database="dbms" 
)
cursor = db.cursor()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',pid=p_id)
@app.route('/home')
def ho():
    return render_template('index.html')


@app.route('/reg')
def registration():
    return render_template('form.html')




@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('ph')  # Corrected field name
        program_id = request.form.get('pg')  # Corrected field name

        # Insert data into the MySQL table
        insert_query = "INSERT INTO participants(name, lname, email, phone, program_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, lname, email, phone, program_id))
        db.commit()
        select_query="select p_id from participants where name=%s"
        cursor.execute(select_query,(name,))
        p_id = cursor.fetchone()[0]
        return render_template('success.html',pid=p_id)

    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error: {e}")
        db.rollback()  # Rollback the transaction in case of an error
        return "An error occurred while processing your request."


@app.route('/update')
def user_details_form():
    return render_template('user_details_form.html')

# Handle form submission
@app.route('/update_profile', methods=['POST'])
def submit_user_details():
    try:
        # Get form data
        p_id = request.form.get('p_id')
        name = request.form.get('name')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Update user details in the database
        update_query = "UPDATE participants SET name = %s, lname = %s, email = %s, phone = %s WHERE p_id = %s"
        cursor.execute(update_query, (name, lname, email, phone, p_id))
        db.commit()

        return render_template('upsuccess.html')

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return "An error occurred while updating user details."

@app.route('/del_v')
def dell():
    return render_template('delete_form.html')  
@app.route('/delete', methods=['POST'])
def delete():
    p_id = request.form.get('p_id')  # Assuming you have an 'id' field in your table
    # Delete data from the MySQL table
    delete_query = "DELETE FROM participants WHERE p_id = %s"
    cursor.execute(delete_query, (p_id,))
    db.commit()

    return f"User details for Participant ID {p_id} deleted successfully."

@app.route('/selpid')
def select_pid():
    return render_template('select_pid.html')


@app.route('/dbm')
def dbmsssss():
    return render_template('dbmss.html')
#<a href="/group_program">dis table!!</a>
@app.route('/group_program')
def groups():
    cursor.execute("select * from participants")
    data=cursor.fetchall()
    return render_template("groupp.html",data=data)
    
@app.route('/sss')
def g():
    try:
        opn = request.args.get("program_id")
        # Fetch all participants from the database
        cursor.execute("SELECT * FROM participants")
        data = cursor.fetchall()
        query="select * from participants where program_id=%s"
        cursor.execute(query,(opn,))
        grouped_participants= cursor.fetchall()
        return render_template("g.html", participant=grouped_participants)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request."
        
    '''
        # Organize participants based on program ID
        grouped_participants = {}
        for participant in data:
            p_id, name, lname, email, phone, program_id = participant
            if program_id in grouped_participants:
                grouped_participants[program_id].append({
                    'p_id': p_id,
                    'name': name,
                    'lname': lname,
                    'email': email,
                    'phone': phone,
                    })
            else:
                grouped_participants[program_id] = [{
                    'p_id': p_id,
                    'name': name,
                    'lname': lname,
                    'email': email,
                    'phone': phone,
                    }]
    '''
        
     
    
if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/update_profile/<int:p_id>', methods=['GET'])
# def render_update_profile(p_id):
#     try:
#         # Create a cursor within a context manager
#         with db.cursor() as cursor:
#             # Fetch participant information from the database based on p_id
#             # This query is an example; adjust it based on your actual database schema
#             participant_query = "SELECT name, lname, email FROM participants WHERE p_id = %s"
#             cursor.execute(participant_query, (p_id,))
#             participant_data = cursor.fetchone()

#             if participant_data:
#                 # Render the update profile form with participant data
#                 return render_template('update_profile.html', p_id=p_id, participants=participant_data)
#             else:
#                 return "Participant not found."

#     except Exception as e:
#         print(f"Error: {e}")
#         return "An error occurred while processing your request."

# # Route to handle the profile update
# @app.route('/update_profile/<int:p_id>', methods=['POST'])
# def update_profile(p_id):
#     try:
#         new_first_name = request.form.get('name')
#         new_last_name = request.form.get('lname')
#         new_email = request.form.get('email')

#         # Create a cursor within a context manager
#         with db.cursor() as cursor:
#             # Update profile in the MySQL table
#             update_query = "UPDATE participants SET fname = %s, lname = %s, email = %s WHERE p_id = %s"
#             cursor.execute(update_query, (new_first_name, new_last_name, new_email, p_id))
#             db.commit()

#         return redirect(url_for('index'))

#     except Exception as e:
#         print(f"Error: {e}")
#         db.rollback()  # Rollback the transaction in case of an error
#         return "An error occurred while processing your request."



# if __name__ == '__main__':
#     app.run(debug=True)
