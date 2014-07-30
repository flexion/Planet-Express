import sys
import json

from settings import settings
from Navigation import navigation


if __name__ == '__main__':

    #
    # Initialization
    #

    ARG = 0

    def next_arg():
        global ARG
        ARG += 1
        return sys.argv[ARG]

    action = next_arg()
    object = next_arg()

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

    import settings.settings as settings

    nav = navigation.Navigator(region='DFW')
    nav.log_in(username=settings.ACCOUNTS['rax-ord-ng']['USERNAME'],
                     api_key=settings.ACCOUNTS['rax-ord-ng']['API_KEY'])

    #
    # Run
    #

    if action == 'get':
        if object == 'servers':
            nav.get_servers()
            print nav.dump_json(nav.ng_servers)
        if object == 'server':
            pass
        if object == 'images':
            nav.get_images()
            print nav.dump_json(nav.images)
        if object == 'image':
            nav.get_images()
            image_id = next_arg()
            print nav.dump_json(nav.get_image_by_id(image_id))
    elif action == 'add':
        if object == 'image':
            if next_arg() == 'member':
                tenant = next_arg()
                image = next_arg()
                print nav.add_image_member(image_id=image,
                                           tenant_id=tenant)['status_code']
                members = nav.get_image_members(image)['text']
                print nav.dump_json(json.loads(members))
