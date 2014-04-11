from settings import settings

import Navigation.navigation


leela = Navigation.navigation.Navigator()
leela.log_in(username=settings.ACCOUNTS['rax-ord-ng']['USERNAME'],
             api_key=settings.ACCOUNTS['rax-ord-ng']['API_KEY'])
