from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo_models
import donation_main
from PIL import Image
# from smartfields import fields
# from smartfields.dependencies import FileDependency
# from smartfields.processors import ImageProcessor
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.http import HttpResponseRedirect
import re
from io import BytesIO
import pytesseract
from django.urls import reverse


class Apply(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    aadhaar_number = models.CharField(unique=True,blank=False,max_length=12)
    phone_number = models.CharField(blank=False,max_length=10)
    published = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField()
    lon = models.FloatField()
    lat = models.FloatField()
    aadhaar_image = models.ImageField(upload_to='aadhaar_image',blank=True)
    # aadhaar_image = fields.ImageField(upload_to='aadhaar_image', dependencies=[
    #     FileDependency(attname='', processor=ImageProcessor(
    #         format='JPEG', 
    #         scale={'max_width': 500, 'max_height': 500})),])
    location = geo_models.PointField(null=True, blank=True, srid=4326, verbose_name='Location')
    special_key = models.CharField(max_length=30)
    request_sent = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    subdistrict = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    state = models.CharField(max_length=64)

    def __str__(self):
        return str(self.first_name)
    
    def save(self,request):
        try:
            print("resizing")
            mywidth = 500

            im = Image.open(self.aadhaar_image)
            wpercent = (mywidth/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            output = BytesIO()

            aadhaar_number_processed = [x for x in str(request.session["aadhaar_number"])]
            aadhaar_number_processed.insert(4,' ')
            aadhaar_number_processed.insert(9,' ')
            aadhaar_number_processed = ''.join(aadhaar_number_processed)

            x = pytesseract.image_to_osd(im)
            ang = int(re.search('(?<=Rotate: )\d+', x).group(0))
            im = im.rotate(360-ang)
            txt = pytesseract.image_to_string(im)
            print(txt)
            if aadhaar_number_processed not in txt or str(request.session["dob"])[:4] not in txt:  

                return False            

            im = im.resize((mywidth,hsize), Image.ANTIALIAS)

            im.save(output, format='PNG', quality=90)

            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.aadhaar_image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.aadhaar_image.name.split('.')[0], 'image/png',
                                            sys.getsizeof(output), None)
        except Exception as e:
            print(e)
            pass
        
        super(Apply, self).save()

class RequestManager(models.Manager):

    def send_req(self,aadhaar_number,donor_id):
        request = Request(donor_id=donor_id, applicant=Apply.objects.get(aadhaar_number=aadhaar_number))
        request.save()

    def remove_req(self,aadhaar_number,donor_id):
        Request.objects.get(donor_id=donor_id, applicant=Apply.objects.get(aadhaar_number=aadhaar_number)).delete()


class Request(models.Model):
    applicant = models.ForeignKey(Apply,on_delete=models.CASCADE)
    donor = models.ForeignKey('donation_main.Donate',on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    manager = RequestManager()

    def __str__(self):
        return self.applicant.first_name

    



# class State(models.Model):
#     name = models.CharField(max_length=64)

#     def __str__(self):
#         return self.name
    
# class District(models.Model):
#     name = models.CharField(max_length=64)
#     state = models.ForeignKey(State,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.name

# class Subdistrict(models.Model):
#     name = models.CharField(max_length=64)
#     district = models.ForeignKey(District,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.name
