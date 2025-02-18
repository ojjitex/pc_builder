from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm
from app.utils import fetch_ozon_data, fetch_ozon_data_by_query
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # В реальном проекте используйте хеширование паролей
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный email или пароль.', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data, password=form.password.data)  # В реальном проекте используйте хеширование паролей
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/components/<category>')
def components(category):
    page = int(request.args.get('page', 1))  # Получаем номер страницы из URL
    per_page = 6  # Количество товаров на странице
    sort_by = request.args.get('sort', 'price_asc')

    try:
        products = fetch_ozon_data(category)
        if sort_by == 'price_asc':
            products.sort(key=lambda x: x['price'])
        elif sort_by == 'price_desc':
            products.sort(key=lambda x: x['price'], reverse=True)
        elif sort_by == 'rating':
            products.sort(key=lambda x: x.get('rating', 0), reverse=True)

        # Разбиение товаров на страницы
        total_pages = (len(products) // per_page) + (1 if len(products) % per_page > 0 else 0)
        paginated_products = products[(page - 1) * per_page: page * per_page]

        return render_template(
            'components.html',
            products=paginated_products,
            current_page=page,
            total_pages=total_pages
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.index'))

@main.route('/components/<category>')
def components(category):
    sort_by = request.args.get('sort', 'price_asc')
    try:
        products = fetch_ozon_data(category)
        recommendations = fetch_compatible_products(category)  # Новая функция для рекомендаций
        return render_template('components.html', products=products, recommendations=recommendations)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.index'))

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        flash('Введите поисковый запрос.', 'warning')
        return redirect(url_for('main.index'))
    try:
        products = fetch_ozon_data_by_query(query)
        return render_template('components.html', products=products)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.index'))