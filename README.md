# Kijiji-Online-Price-Tracker
Server based tool that tracks for given products in Kijiji and alerts users via email when available. 
url=https://www.kijiji.ca/b-canada/onewheel/k0l0?rb=true&dc=true

Many online business persons need some kind of product tracker, price tracker or sniper tool that would alert them when a product is available. 
In this case, the user enters their email creds and the email address that would receive the notifications. 
The user also enters the target location and  search keywords.
The tool runs on a Google Cloud Function every 5 minutes, checks for posted ads, compares it to the first dataset in a Google sheet, if there's an update, the user gets a 
notification with the details of the product.
