**This OCI Functions will create a pre authenticated URL to the uploaded object in the bucket and send that URL via email.**

**Requirement:**
Customers wanted cost usage reports needs to be sent over an email. In OCI scheduled Cost usage report, which will be automatically sent to Object storage bucket with specific permission to the bucket.

**Process:**
Event rule needs to trigger the function whenever the upload happens the Object storage bucket.

**Create a Function:**
In OCI, create an Application by providing network details(VCN and subnet) and shape as GENERIC_X86.
Under the application we need to deploy the Function. To do that, follow the steps mentioned in the Getting started. Select Cloudshell and follow the process.
Since this function is written in python wherever it is mentioned as java provide that as python.
Inside the folder (whichever created) func.py will be available , edit the script and paste the code from above folder.

<img width="228" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/85653d5d-5431-432e-b53a-7859c1cfa285">
<img width="202" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/001f0d7b-5a96-4bef-8230-ae8dba7f43d7">


Once after saving deploy the function using the command mentioned in the console.

"fn -v deploy --app <app name>

Folder name sam & App name is also and deployed the same. We can see that in OCI console as below.
<img width="1144" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/7b56119d-4f58-4f8b-8324-ba20f454b869">

Once function is deployed succesfuuly move to next steps to Invoke the function. 

**Create Events rule:** In OCI needs to trigger the function whenever the object/file gets uploaded into bucket.
Object create and Object upload event type created on the attribute i.e., specific bucket.

<img width="1156" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/6c69c0cf-9597-44e4-bfdf-4d0d6d2255af">
Create the action to trigger the function.

<img width="908" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/ef04ba22-bed3-4797-8fd2-7e0568896648">

**Configuration**

Need few service level permission at Function level process this.

Create a dynamic group with below matching rules.

"ALL {resource.type = 'fnfunc', resource.compartment.id = '<COMPARTMENT_ID>'}"

Create policy under the same compartment where the function is available.

<img width="1035" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/91a87637-cc14-4bd5-8067-a46879c4077a">

With all these set up , Function will be invoked and create the pre authenticated url.

**Email configuration:**
To send the email you have to create Email domain for your Public domain. 
In this example, we have had public domain(DNS) called sehna.cloud.

Followed the below blog to set up the email domain and configured it.
https://blogs.oracle.com/cloud-infrastructure/post/step-by-step-instructions-to-send-email-with-oci-email-delivery

EMAIL DOMAIN
<img width="1367" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/6cbb97d3-85b6-4775-b8aa-22fc7248f759">

DKIM configuration: It provides Cname and Cvalue. Need to be configured at DNS level by adding records. (Follow the blog)

<img width="624" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/b53c266b-1cfe-4264-8a4e-ebf9073beb3e">

Approved sender: create sender email under approved sender and it provides SPF details. Configure SPF in DNS by adding record(Follow the blog)

<img width="737" alt="image" src="https://github.com/samrathasp47/samrathasp47/assets/163320158/fc08c0c6-8c01-4420-9b22-ce05427e02d4">

For the logging purpose to check the error in function invoke, you can enable Logging under Application.

**InvokeFunction**

To test this , upload the file or any object into the specific bucket . You should receive email. If not received please check the logs whichever enabled at the Application level.










