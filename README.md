# Mailer

Mailer is a lightweight web based application for sending emails, using different email providers. It was developed by [Georgi Zhuhov] as a coding challange in the application process for [Uber].
  - Open the demo web site: http://37.139.11.108/
  - Send an email

Mailer is using multiple backend email services for sending emails. If any of them fails, it will continue with the task until an email is successfully delivered. In this way, it aims to provide a service with 0% drop rate.

The following email services are implemented:
* [Mandrill]
* [Mailgun]

It can be easily extended with different email services using the provided base classes and abstractions.

### Version
1.0.0

### Tech

Mailer uses a number of open source projects to work properly:

##### [Django]
Django provides email manager, but doesn't provide a multiple backends. The project can be used as an additional backend, which will guarantee that the emails will be always delivered.

##### [SCSS]
In the future if the project starts growing up, the css will become too big and imposible to maintain. With SCSS you are a step closer to the perfection.

##### [jQuery]
Simple and the most popular framework in the world. Part from most of the modern js frameworks. A good base for future development.

Mailer itself is open source with a [public repository][mailer]
 on GitHub.

### Installation

You will need python3.4 or above installed.
```sh
$ git clone [git-repo-url]
$ cd mailer
$ pip install -r requirements.txt
```
### Extending

To add a new email engine, you have to inherit mailer.utils.engines.EmailEngineInterface and implement the required functions. Note that the created class should be also mentioned in the settings file as a string import. Example:
```py
EMAIL_ENGINES = [
    'your.custom.engine',
    'mailer.utils.engines.MandrillEmailEngine',
    'mailer.utils.engines.MailGunEmailEngine',
]
```

### Demo

Demo application can be found on this address:
http://37.139.11.108/
Hosted in [DigitalOcean]

### TODO

The functionality is quite limited at this point - sending text messages with basic html tags. There are many to do things, which can be added, e.g:
 * Attachments
 * BCC
 * Draft box
 * Account model


   [DigitalOcean]: <https://www.digitalocean.com>
   [mailer]: <https://github.com/SpeeDly/mailer>
   [Uber]: <https://www.uber.com/>
   [git-repo-url]: <https://github.com/SpeeDly/mailer.git>
   [Georgi Zhuhov]: <https://github.com/SpeeDly>
   [Mandril]: <https://www.mandrill.com/>
   [Mailgun]: <https://mailgun.com/>
   [Django]: <https://www.djangoproject.com/>
   [SCSS]: <http://sass-lang.com/>
   [jQuery]: <http://jquery.com>