"""Routes."""
from flask import render_template, request, Response, session, redirect

from app import app, CURRENT_USER_SESSION_KEY
from models import User, db, Client, Account, AccountType
from auth import is_authenticated


@app.route('/', methods=['GET'])
def index():
    if CURRENT_USER_SESSION_KEY in session:
        return redirect('/clients')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user is None:
        return Response(response='User not found!')
    else:
        if user.compare_password(password):
            session[CURRENT_USER_SESSION_KEY] = user.email
            return redirect('/clients')
        else:
            return Response(response='Email/password didn\'t match!')


@app.route('/logout', methods=['GET'])
@is_authenticated
def logout():
    if CURRENT_USER_SESSION_KEY in session:
        session.pop(CURRENT_USER_SESSION_KEY, None)
        return redirect('/')


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    user = User(name, email, password)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return Response(response=user.name + ' user created!')


@app.route('/clients', methods=['GET', 'POST'])
@is_authenticated
def clients():
    if request.method == 'GET':
        all_clients = Client.query.all()
        return render_template('client_list.html', clients=all_clients)
    else:
        name = request.form['name']
        email = request.form['email']

        client = Client(name, email)
        db.session.add(client)
        db.session.commit()
        db.session.refresh(client)
        return redirect('/clients/' + str(client.id))


@app.route('/clients/add', methods=['GET'])
@is_authenticated
def add_client():
    return render_template('client_edit.html', client=None)


@app.route('/clients/<id>', methods=['GET', 'POST'])
@is_authenticated
def client_detail(id):
    if request.method == 'GET':
        client = Client.query.get(id)
        linked_accounts = Account.query.filter((Account.client1 == client.id) |
                                               (Account.client2 == client.id)).all()
        print(linked_accounts)
        return render_template('client_edit.html', client=client,
                               linked_accounts=linked_accounts)
    else:
        client = Client.query.get(id)
        client.name = request.form['name']
        client.email = request.form['email']
        db.session.commit()
        return redirect('/clients/' + str(client.id))


@app.route('/accounts', methods=['GET', 'POST'])
@is_authenticated
def accounts():
    if request.method == 'GET':
        all_accounts = Account.query.all()
        for account in all_accounts:
            account.client1 = Client.query.get(account.client1)
            if account.client2 is not None:
                account.client2 = Client.query.get(account.client2)

        return render_template('account_list.html', accounts=all_accounts)
    else:
        # TODO: Complete create account process
        acc_no = request.form['acc_no']
        acc_name = request.form['acc_name']
        acc_type = AccountType.SAVINGS if request.form['acc_type'] == AccountType.SAVINGS.value \
            else AccountType.CURRENT
        client1_email = request.form['client1']
        client2_email = request.form['client2']

        client1 = Client.query.filter_by(email=client1_email).first()
        client2 = None
        if len(client2_email) > 0:
            client2 = Client.query.filter_by(email=client2_email).first()
            client2 = client2.id if client2 is not None else None

        if client1 is not None:
            client1 = client1.id
            new_account = Account(acc_no, acc_name, acc_type, client1, client2)
            db.session.add(new_account)
            db.session.commit()
            db.session.refresh(new_account)
            return render_template('account_edit.html', account=new_account)
        else:
            return Response('Error in form!')


@app.route('/accounts/add', methods=['GET'])
@is_authenticated
def add_account():
    return render_template('account_edit.html', account=None)


@app.route('/accounts/<acc_no>', methods=['GET', 'POST'])
@is_authenticated
def account_detail(acc_no):
    if request.method == 'GET':
        account = Account.query.filter_by(acc_no=acc_no).first()
        account.client1 = Client.query.get(account.client1)
        print(account.client1)
        if account.client2 is not None:
            account.client2 = Client.query.get(account.client2)
        return render_template('account_edit.html', account=account)
    else:
        account = Account.query.filter_by(acc_no=acc_no).first()
        account.acc_no = request.form['acc_no']
        account.acc_name = request.form['acc_name']
        account.acc_type = AccountType.SAVINGS if request.form['acc_type'] == AccountType.SAVINGS.value \
            else AccountType.CURRENT
        db.session.commit()
        return redirect('/accounts/' + str(account.acc_no))
