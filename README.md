# فروشگاه اینترنتی فارسی


## نحوه پیکربندی و استفاده از پروژه

در مرحله اول نیاز به ساخت یک محیط مجازی(virtual env) جهت اجرا پروژه  دارید که می‌توانید با توجه سیستم عامل خود به صورت زیر عمل کنید:

به مسیر پروژه رفته و ترمینال یا cmd را در آن اجرا کنید و دستور زیر را وارد کنید:

```sh
python -m venv venv
```

حالا باید محیط مجازی که ساختید را فعال کنید

در **Linux/MacOs**

```sh
source venv/bin/activate
```

در **Windows**

```sh
venv/Scripts/activate
```

در مرحله بعد باید وابستگی‌های(dependency) پروژه را نصب کنید

```sh
pip install -r requirments.txt
```

## نحوه اجرای پروژه
برای اجرای پروژه می‌توانید از طریق زیر عمل کنید

فایلی به نام *env.* ساخته و مقادیری مانند فایل *env-sample.* در قرار بدهید.

در مرحله بعد دستور زیر را جهت ساخت دیتابیس و جداول آن انجام دهید

```sh
python manage.py migrate
```

در نهایت دستور زیر را وارد کنید تا پروژه ران شود و از طریق این [Link](http://127.0.0.1:8000) به آن مراجعه کنید


```sh
python manage.py runserver
```