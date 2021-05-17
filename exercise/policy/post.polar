allow(_actor, "view", post: exercise::Post) if
    post.access_level = exercise::Post.ACCESS_PUBLIC;

allow(actor: exercise::Profile, "view", post: exercise::Post) if
    post.access_level = exercise::Post.ACCESS_PRIVATE and
    post.created_by = actor;