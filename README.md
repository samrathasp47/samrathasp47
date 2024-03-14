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

Once after saving deploy the function using the command mentioned in the console.

"fn -v deploy --app <app name>"

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








