<?php

class comment{
    public function user()
  {
        return $this->belongsto(User::class);
    }

    public function blog()
    {
        return $this->belongsTo(Blog::class);
    }

    public function get_comments()
    {
        return $this->hasMany(Comment::class, 'parent_id');
    }

    public function comment()
    {
        return $this->belongsTo(Comment::class, 'parent_id');
    }
}

?>