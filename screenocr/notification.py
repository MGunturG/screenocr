from winsdk.windows.data.xml.dom import XmlDocument
from winsdk.windows.ui.notifications import ToastNotificationManager, ToastNotification

xml_template = '''
<toast activationType="protocol" launch="http:" scenario="{scenario}">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>
'''

def add_text(msg, document):
    if isinstance(msg, str):
        msg = {
            'text': msg
        }
    binding = document.select_single_node('//binding')
    text = document.create_element('text')
    for name, value in msg.items():
        if name == 'text':
            text.inner_text = msg['text']
        else:
            text.set_attribute(name, value)
    binding.append_child(text)


def add_image(img, document):
    if isinstance(img, str):
        img = {
            'src': img
        }
    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    for name, value in img.items():
        image.set_attribute(name, value)
    binding.append_child(image)


def show_notif(appid, title, message):
    document = XmlDocument()
    document.load_xml(xml_template.format(scenario='default'))

    add_text(title, document=document)
    add_text(message, document=document)
    
    notification = ToastNotification(document)
    notifier = ToastNotificationManager.create_toast_notifier(appid)
    
    notifier.show(notification)