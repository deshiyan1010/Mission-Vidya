from django.db import models
from django.contrib.auth.models import User
from apply_main.models import Apply
from django.core.exceptions import ValidationError
# from smartfields import fields
# from smartfields.dependencies import FileDependency
# from smartfields.processors import ImageProcessor
#from s3direct.fields import S3DirectField
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from PIL import Image


class Donate(models.Model):
    model_name = models.CharField(max_length=264)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='',null=True,blank=True)
    published = models.DateTimeField(auto_now_add=True)
    donated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.model_name

class Images(models.Model):

    mobile_images = models.ImageField(upload_to='donation_main',blank=True)
    #mobile_images = S3DirectField(dest='primary_destination', blank=True)
    # mobile_images = fields.ImageField(upload_to='donation_main', dependencies=[
    #     FileDependency(attname='', processor=ImageProcessor(
    #         format='JPEG', 
    #         scale={'max_width': 500, 'max_height': 500})),])
    donation = models.ForeignKey(Donate,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.donation.id)

    def save(self):

        mywidth = 500
        # Opening the uploaded image
        im = Image.open(self.mobile_images)
        wpercent = (mywidth/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        output = BytesIO()

        # Resize/modify the image
        im = im.resize((mywidth,hsize), Image.ANTIALIAS)
        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.mobile_images = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.mobile_images.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(Images, self).save()


class DonatedInformation(models.Model):
   
    device = models.ForeignKey(Donate,on_delete=models.CASCADE)
    receiver = models.ForeignKey(Apply,on_delete=models.CASCADE)
    donated_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.receiver.first_name
    