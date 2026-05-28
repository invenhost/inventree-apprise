# inventree-apprise

Send notifications from InvenTree via Apprise

## Setup

1. Install this plugin in the webinterface with the packagename `inventree-apprise`

1. Enable the plugin in the plugin settings. You need to be signed in as a superuser for this.
**The server will reload all plugins if you enable the plugin**

1. Add all endpoints you want to use in the plugin settings. You can use the [Apprise URL Syntax](https://github.com/caronc/apprise#supported-notifications). The Apprise project also provides an [interactive URL builder](https://appriseit.com/url-builder/). That can be used to generate the URL for you. The plugin settings are available under the following site in >1.0 setup: /web/settings/admin/plugin/apprise/

## Compatibility

| plugin version | InvenTree version |
|----------------|-------------------|
| <=1.2 | pre 1.0 |
| 1.3 | 1.3.1+ |

## License
This project is licensed as MIT. Copy and do what you want - maybe tag your new plugin so others can find it. The more the merrier.
