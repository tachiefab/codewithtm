from rest_framework import generics, mixins, permissions, status
# from rest_framework.response import Response
# from django.contrib.contenttypes.models import ContentType
# from .serializers import LikeSerializer
# from .models import Like
# from posts.models import Post


# class LikeAPIView(generics.GenericAPIView): 
# 	permission_classes = [permissions.AllowAny]
# 	serializer_class = LikeSerializer

# 	def get(self, request, type, obj_id):
# 		if obj_id:
# 			model_type      = Post
# 			model_qs        = ContentType.objects.filter(model=model_type)
# 			# print(model_qs)

# 			c_type = ContentType.objects.get_for_model(model_type)

# 			if model_qs.exists():  
# 				SomeModel       = model_qs.first().model_class()
# 				obj_qs          = SomeModel.objects.filter(id=obj_id)
# 				if obj_qs.exists():
# 					content_obj     = obj_qs.first()
# 					print(content_obj)
# 					pk = content_obj.id
# 					like_qs = Like.objects.get(content_type=c_type, object_id=pk)
# 					print(like_qs)
# 				# try:
# 				# 	pk = content_obj.id
# 				# 	like_qs = Like.objects.get(content_type=SomeModel, object_id=pk)
# 				# 	print(like_qs)
# 				# except:
# 				# 	pass
# 	                # if like_qs:
# 	                #     if request.user.is_authenticated:
# 	                #         is_liked = Like.objects.like_toggle(request.user, sender, like_qs)
# 	                #         return Response({
# 	                #                         'liked': is_liked,
# 	                #                         'likes_count': like_qs.likes_count
# 	                #                         }
# 	                #                         )
# 					# print(content_obj)
# 		# return Response({"message": message}, status=400)
# 		return Response(status=status.HTTP_200_OK)