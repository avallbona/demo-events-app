# Fixed issues

- Project was configured to spanish
- No unique constraint on EventAttendee model
- Can join multiple times (e.g by pre-loading multiple tabs)
- Can cause 500 when withdrawing after using the above loophole to sign up multiple times
- Can cause 500 when withdrawing multiple times (e.g by pre-loading multiple tabs)
- Can create events in the past but they do not appear in the list (I would have expected this condition to raise an error)
- Only show first part of email in UI: looks like django-allauth picks the first part of the email as username by default, which gets us half the way there. However allauth just adds digits at the end of the username to avoid clashes.
- Editing the hidden "action" field in the HTML allows me to choose whether I want to sign up or withdraw from an event (regardless of what the form says); no BE validation on this field
