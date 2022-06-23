from pathlib import Path
from bs4 import BeautifulSoup
import pychrome
import base64
import sys
sys.setrecursionlimit(10000) # Required for dumping html for some pages

for file in Path("raw_html").glob("*.html"):
    print(file)
    cleaned_html_path = Path("cleaned_html") / file.name
    pdf_path = (Path("cleaned_pdf") / file.name).with_suffix(".pdf")

    if not cleaned_html_path.exists():
        html_content = open(file, mode='r', encoding='utf-8-sig')
        parsed = BeautifulSoup(html_content, 'html.parser')
        for img in parsed.select("img"):
            img_url = img.get("src")
            img_name = Path(img_url).name
            image_path = Path("Images") / img_name
            img["src"] = f"../Images/{img_name}"

            if not image_path.exists():
                # create a browser instance
                browser = pychrome.Browser(url="http://127.0.0.1:9222")

                # create a tab
                tab = browser.new_tab()

                def response_received(**kwargs):
                    # Only save things that are actually images which have a type of Document
                    if kwargs["type"] == 'Document':
                        response_body = tab.Network.getResponseBody(requestId=kwargs["requestId"])["body"]
                        image_path.write_bytes(base64.b64decode(response_body))

                # When the network recieves a response call this function
                tab.Network.responseReceived = response_received

                # start the tab
                tab.start()

                # call method
                tab.Network.enable()

                # call method with timeout
                tab.Page.navigate(url=img_url, _timeout=5)

                # wait for loading
                tab.wait(1)

                # stop the tab (stop handle events and stop recv message from chrome)
                tab.stop()

        # General clean up
        if asd := parsed.select_one("div[class='print']"):
            asd.decompose()
        if asd := parsed.select_one("button[class='prev section-button']"):
            asd.decompose()
        if asd := parsed.select_one("button[class='next section-button']"):
            asd.decompose()

        # button class="prev section-button"
        cleaned_html_path.write_bytes(parsed.encode("utf-8"))

    # Convert html with wkhtmltopdf
    if not pdf_path.exists():
        import subprocess
        subprocess.run(["C:/Programs/wkhtmltox/bin/wkhtmltopdf.exe", "--enable-local-file-access", str(cleaned_html_path), str(pdf_path)])
