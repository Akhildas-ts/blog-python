
import os
import sys

# this is the entry point like main.go
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings') 
    try:
        # it’s just trying to import Django’s management function.
        from django.core.management import execute_from_command_line
        # exc holds the original error details (so you don’t lose the reason).
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # “when you type a command, this line decides what Django should do.”


if __name__ == '__main__':
    main()
