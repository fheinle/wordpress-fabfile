UPDATE wp_options SET option_value = 'http://localhost/wordpress/' where option_name = 'siteurl';
UPDATE wp_options SET option_value = 'http://localhost/wordpress/' where option_name = 'home';
UPDATE wp_posts SET post_content = REPLACE(post_content, 'staging.example.com', 'localhost');