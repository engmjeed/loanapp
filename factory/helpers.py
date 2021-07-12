from loans.models import Application
from clients.models import Client, LoanProfile
from datetime import date


class Helpers:
    def create_loan_application(self,client,product,amount,period):
        code = self.get_loan_application_next_code()

        return Application.objects.create(
                client = client,
                product = product,
                amount = amount,
                duration = period,
                code = code,)

    def get_latest_loan_application(self):
        try:
            application = Application.objects.latest('created_at')
        except Application.DoesNotExist:
            return None
        else:
            return application



    def get_loan_application_next_code(self):
        today = date.today().isoformat()
        year, month, day = str(today).split('-')

        today_code = str(year)[2:] +  str(month) + str(day)
        next_code = today_code + '1'

        latest = self.get_latest_loan_application()
        if latest and (today_code == str(latest.code)[:6]):
            next_code = latest.code + 1

        return int(next_code)

    def get_client_product_loan_profile(self,client,product):
        return LoanProfile.objects.filter(client=client,product=product).last()

    def get_client_by_msisdn(self,msisdn):
        msisdn = str(msisdn).strip('+').strip()
        try:
            client = Client.objects.get(msisdn=msisdn)
        except Client.DoesNotExist:
            client = None
        return client
            

       


helpers = Helpers()

