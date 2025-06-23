"""
Controllers for the todos module, handling routes for managing and interacting with todos.
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from app.mod_todos.models import (
    add_todo_to_database,
    get_all_todos,
    get_todo_by_id,
    complete_todo_in_database,
    verify_todo_in_database,
    modify_todo_in_database,
    assign_todo_to_user,
    drop_todo_from_database
    
)

mod_todos = Blueprint("todos", __name__, url_prefix="/todos")

# function for rendering the main todos page
@mod_todos.route("/")
def main():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    user_id = session.get("user_id")
    all_todos = get_all_todos()
    return render_template("todos/main.html", todos=all_todos, user_id=user_id)

# Create a new todo for the logged-in user
@mod_todos.route("/new_todo", methods=["GET", "POST"])
def new_todo():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    if request.method == "GET":

        return render_template("todos/new_todo.html")
    
    if request.method == "POST":
        # check csrf token
        form = request.form
        if form["csrf_token"] != session["csrf_token"]:
            flash("Invalid CSRF token.", "danger")
            return redirect(url_for("users.log_in"))
        
        # Get form data and validate
        user_id = session.get("user_id")
        todo = form["todo"]
        description = form["description"]
        todo_score = form["todo_score"]
        due_date = form["due_date"]


        if not todo or not description or not todo_score or not due_date:
            flash("Some required fields are not filled.", "danger")
            return render_template("todos/new_todo.html", todo_entry=form)
        
        if add_todo_to_database(
            user_id=user_id,
            todo=todo,
            description=description,
            todo_score=todo_score,
            due_date=due_date,
        ):
            flash("Todo created successfully!", "success")
            return redirect(url_for("todos.main"))
        else:
            flash("Problem when creating a new todo.", "danger")
            return render_template("todos/new_todo.html", todo_entry=form)
        

# update an existing todo
@mod_todos.route("/update_todo", methods=["GET", "POST"])
def update_todo():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    if request.method == "GET":
        todo_id = request.args.get("todo_id")
        if not todo_id:
            flash("Todo ID is required for updating.", "danger")
            return redirect(url_for("todos.main"))
        
        # get todo by id
        todo_entry = get_todo_by_id(todo_id)
        if not todo_entry:
            flash("Todo not found.", "danger")
            return redirect(url_for("todos.main"))
        
        return render_template("todos/update_todo.html", todo_entry=todo_entry)

    if request.method == "POST":
        # check csrf token
        form = request.form
        if form["csrf_token"] != session["csrf_token"]:
            flash("Invalid CSRF token.", "danger")
            return redirect(url_for("users.log_in"))
        
        # Get form data and validate
        todo_id = request.args.get("todo_id")
        todo = form["todo"]
        description = form["description"]
        todo_score = form["todo_score"]
        due_date = form["due_date"]

        # todo from database pass it to the template if problems
        todo_entry = get_todo_by_id(todo_id)
        
        if not todo or not description or not todo_score or not due_date:
            flash("Some required fields are not filled.", "danger")
            return render_template("todos/update_todo.html", todo_entry=todo_entry)
        
        if modify_todo_in_database(
            todo_id=todo_id,
            todo=todo,
            description=description,
            todo_score=todo_score,
            due_date=due_date,
        ):
            flash("Todo updated successfully!", "success")
            return redirect(url_for("todos.main"))
        else:
            flash("Problem when updating the todo.", "danger")
            return render_template("todos/update_todo.html", todo_entry=todo_entry)
        

# Assign the current user to a todo.
@mod_todos.route("/assign_for_todo", methods=["GET", "POST"])
def assign_for_todo():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    # get user id and todo_id from the request
    todo_id = request.args.get("todo_id")
    user_id = session.get("user_id")
    try:
        assign_todo_to_user(todo_id, user_id)
        flash("Todo assigned successfully!", "success")
        return redirect(url_for("todos.main"))
    except Exception as e:
        flash(f"Failed to assign todo: {str(e)}", "danger")
        return redirect(url_for("todos.main"))

# Mark a todo as completed by the assigned user.
@mod_todos.route("/complete_todo", methods=["GET", "POST"])
def complete_todo():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    user_id = int(session.get("user_id"))
    todo_id = request.args.get("todo_id")
    assigned_to_id = int(request.args.get("assigned_to_id"))
    if not assigned_to_id or assigned_to_id != user_id:
        flash("You are not assigned to this todo.", "danger")
    try:
        complete_todo_in_database(todo_id)
        return redirect(url_for("todos.main"))
    except Exception as e:
        flash(f"Failed to complete todo: {str(e)}", "danger")
        return redirect(url_for("todos.main"))

# Verify a completed todo and update its status.
@mod_todos.route("/verify_todo", methods=["GET", "POST"])
def verify_todo():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    session_user_id = int(session.get("user_id"))
    todo_id = request.args.get("todo_id")
    todo_user_id = int(request.args.get("user_id"))

    if not todo_user_id or todo_user_id != session_user_id:
        flash("You are not authorized to verify this todo.", "danger")
    try:
        verify_todo_in_database(todo_id)
        flash("Todo verified successfully!", "success")
        return redirect(url_for("todos.main"))
    except Exception as e:
        flash(f"Failed to verify todo: {str(e)}", "danger")
        return redirect(url_for("todos.main"))

# Function to handle the deletion of a todo
@mod_todos.route("/delete_todo", methods=["GET", "POST"])
def delete_todo():
    if "user_id" not in session:
        return redirect(url_for("users.log_in"))
    
    todo_id = request.args.get("todo_id")
    if not todo_id:
        flash("Todo ID is required for deletion.", "danger")
    try:
        # Assuming a function delete_todo_from_database exists to handle the deletion
        drop_todo_from_database(todo_id)
        flash("Todo deleted successfully!", "success")
        return redirect(url_for("todos.main"))
    except Exception as e:
        flash(f"Failed to delete todo: {str(e)}", "danger")
        return redirect(url_for("todos.main"))