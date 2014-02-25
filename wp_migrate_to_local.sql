UPDATE wp_options SET option_value = 'http://debian.local' where option_name = 'siteurl';
UPDATE wp_options SET option_value = 'http://debian.local' where option_name = 'home';
UPDATE wp_posts SET post_content = REPLACE(post_content, 'http://demo.florianheinle.de', 'http://debian.local');
