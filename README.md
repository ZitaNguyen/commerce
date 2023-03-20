# Commerce
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a "watchlist".

## Functionalities

### Active Listings Page
* This is the default route of the web application. 
* Users view all of the currently active auciton listings.

### Listing Page
* Click on a listing should take users to a page specific to that listing. On that page, users can view all details about the listing, including the current price for the listing.
* If the user is signed in, the user can add the item to their "watchlist". If the item is already on the watchlist, the user can remove it.
* If the user is signed in, the user can bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn't meet those criteria, the user is presented with an error.
* If the user is signed in and is the one who created the listing, the user can "close" the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
* If a user is signed in on a closed listing page, and the user has won that auction, the page say so.
* Users who are signed in can add comments to the listing page. The listing page displays all comments that have been made on the listing.

### Watchlist
* Users who are signed in can visit a "watchlist" page, which displays all of the listings that a user has added to their watchlist.

### Create Listing
* Users can create a new listing with title, description, starting bid.
* Users can optionally provide a URL for an image for the listing and/or a category.

### Categories
* Users can visit a page that displays a list of all listing categories.
* Clicking on the name of nay category takes the user to a page that displays all of the active listings in that category.

### Django Admin Interface
* A site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.

### Models
* User
* Listing
* Category
* Bid
* Comment
* Watchlist

