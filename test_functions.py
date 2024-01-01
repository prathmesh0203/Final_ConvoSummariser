from capp_new import create_top_ten_labels

# labels = ['Restaurant Experience and Recommendation', 'Cuisine Inquiry', 'Dining Suggestion', 'Car Buying Inquiry','Car', 'Vehicle Preference Discussion', 
# 'Family Trip Planning', 'Travel Destination Recommendation', 'General Preferences', 'nike', 'adidas', 'Nike Shoes', 'Adidas Shoes','Travelling']

# labels2 = ['Automobile', 'Car', 'Vehicle', 'Transportation', 'Sedan', 'Nutrition', 'Diet', 'Healthful Eating', 'Wellness', 'Fitness', 'Exercise', 'Workout', 'Physical Activity', 'Technology', 'Innovation', 'Software Development', 'Programming', 'Coding']

# # print(create_top_ten_labels(labels2))
# print(f"Length of labels:{len( labels2)}")
# print(f"Length of top ten labels:{len(create_top_ten_labels(labels2))}")

# print(create_top_ten_labels(labels2))

all_labels = {'Greetings and Assistance', 'Color and Style Preference', 'Feedback - User Interface', 'Order Issue - Damaged Goods', 'Product Inquiry - Organic Options', 'Promotions and Offers', 'Product Inquiry', 'Festival Related Inquiry', 'Website Navigation Assistance', 'Product Availability', 'Running Shoes Specifications', 'Order Issue - Missing Items', 'Food and Cuisine', 'Customer Service', 'Ordering Process', 'Customer Inquiry', 'Order Issue - Late Delivery', 'Order Confirmation', 'Product Features and Details', 'Product Recommendation', 'Size Specification', 'Customer Service Inquiry', 'Brand Preference'}

top_labels = create_top_ten_labels(list('all_labels'))
print(top_labels)


