from ProductDetails import ProductDetails
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

MY_EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('PASSWORD')


def send_email(message: str) -> None:

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        # Secure the connection
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="amgedelshiekh@gmail.com",
                            msg=message)


if __name__ == '__main__':
    url = "https://www.amazon.co.jp/-/en/Gaming-Laptop-G513IE-Eclipse-G513IE-R7R30/dp/B09MYYMVQM/?_encoding=UTF8&pd_rd_w=57raA&pf_rd_p=baf93712-734c-4342-ae03-33b258824a43&pf_rd_r=ANSYAME74DKD0N2KA4RG&pd_rd_r=147abe11-7ef6-4560-82a0-e4c3831fcefc&pd_rd_wg=Glmcw&ref_=pd_gw_ci_mcx_mr_hp_atf_m"

    desired_price = 180000
    item = ProductDetails(url)
    if item.price <= desired_price:
        message = f"Subject:Price Drop Alert\n\n{item.name} price has gone below {desired_price}{item.price_unit}. Now the price is {item.price_details} only. Maybe you can consider buying now. Go to the URL\n{item.get_url()}."
        message = message.encode("utf-8")

        send_email(message)
