UPDATE wp_options SET option_value = 'http://demo.florianheinle.de/stura/' where option_name = 'siteurl';
UPDATE wp_options SET option_value = 'http://demo.florianheinle.de/stura/' where option_name = 'home';
UPDATE wp_posts SET post_content = REPLACE(post_content, 'debian.local', 'demo.florianheinle.de');
