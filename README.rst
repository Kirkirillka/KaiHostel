=====
KaiHostel3
=====

=====
KaiHostel3 is my own blog.That is enough for you to know.
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "Blog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        '=====
KaiHostel3',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^Blog/', include('Blog.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/KaiHostel3/ to participate in the Blog.
