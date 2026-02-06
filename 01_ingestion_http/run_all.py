from auth.basic_auth import run as auth_run
from cookies.cookies_session import run as cookies_run
from extraction.get_json import run as json_run
from extraction.get_xml import run as xml_run
from extraction.get_html import run as html_run
from forms.post_form import run as form_run
from errors.handle_403 import run as error_run
from redirects.follow_redirect import run as redirect_run

def main():
    print("Running HTTP ingestion scenarios...\n")

    auth_run()
    cookies_run()
    json_run()
    xml_run()
    html_run()
    form_run()
    error_run()
    redirect_run()

    print("\nAll scenarios executed successfully")

if __name__ == "__main__":
    main()
