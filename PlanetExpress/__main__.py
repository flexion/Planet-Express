import sys
import json

from settings import settings
from Navigation import navigation


if __name__ == '__main__':

    USAGE = '''
   - Description -

This app provides some scaffolding to work with the Rackspace cloud in Python.

   - Usage -

Options are supplied via natural language syntax. Here's what's currently supported...

get
    server <server id>
    servers
    image <image id>
    images
    loadbalancers

add
    network <server id> <network id>
    image
        member <tenant id> <image id>


    '''

    #
    # Initialization
    #

    ARG = 0

    def next_arg():
        global ARG
        ARG += 1
        try:
            return sys.argv[ARG]
        except:
            print 'ERROR! Required argument not supplied, got: "' + ''.join(sys.argv[1:]) + '"...'
            print USAGE
            exit(1)

    action = next_arg()
    object = next_arg()

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

    import settings.settings as settings

    nav = navigation.Navigator(region=settings.ACCOUNTS['rax-ord-ng']['REGION'])
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
        if object == 'loadbalancers':
            nav.get_load_balancers()
            print nav.dump_json(nav.loadbalancers)
    elif action == 'add':
        if object == 'image':
            if next_arg() == 'member':
                tenant = next_arg()
                image = next_arg()
                print nav.add_image_member(image_id=image,
                                           tenant_id=tenant)['status_code']
                members = nav.get_image_members(image)['text']
                print nav.dump_json(json.loads(members))
        if object == 'network':
            network_id = next_arg()
            print nav.dump_json(nav.get_image_by_id(network_id))
