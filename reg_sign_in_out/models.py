from django.db import models
from django.contrib.auth.models import User
from apply_main.models import *
from django.contrib.gis.db import models as geo_models

# from smartfields import fields
# from smartfields.dependencies import FileDependency
# from smartfields.processors import ImageProcessor

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from PIL import Image

class Registration(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)
    # profile_pic = fields.ImageField(upload_to='profile_pic', blank=True, dependencies=[
    #     FileDependency(attname='', processor=ImageProcessor(
    #         format='JPEG', 
    #         scale={'max_width': 500, 'max_height': 500})),])
    phone_number = models.CharField(blank=False,max_length=10)
    lon = models.FloatField()
    lat = models.FloatField()
    location = geo_models.PointField(null=True, blank=True, srid=4326, verbose_name='Location')
    subdistrict = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    
    def __str__(self):
        return self.user.username
    
    def save(self):
        try:
            mywidth = 500
            # Opening the uploaded image
            im = Image.open(self.profile_pic)
            wpercent = (mywidth/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            output = BytesIO()

            # Resize/modify the image
            im = im.resize((mywidth,hsize), Image.ANTIALIAS)
            # after modifications, save it to the output
            im.save(output, format='JPEG', quality=90)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.profile_pic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.profile_pic.name.split('.')[0], 'image/jpeg',
                                            sys.getsizeof(output), None)
        except:
            pass
        
        super(Registration, self).save()