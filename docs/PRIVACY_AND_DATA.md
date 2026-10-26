# Privacy and local data

CampusFlow handles face images and attendance records. Treat both as sensitive personal information.

## Files created by the app

| Path | Contents | Git status |
| --- | --- | --- |
| **data/attendance.sqlite3** | People, course details, attendance and exit history | Ignored |
| **data/faces/<profile-id>/** | Captured face sample images | Ignored |
| **models/final_model.h5** | Trained recognition model | Ignored |
| **models/labels.json** | Local model-to-profile mapping | Ignored |
| **\*_attendance.csv**, **\*_exit.csv**, **registered_people.csv** | Exported records | Ignored |

The Haar cascade file in **models/** is application code, not a student record.

## Deletion and recovery

Moving a person to the Recycle Bin marks the profile as inactive but keeps its face samples, details and attendance history for recovery. Restoring the profile brings those records back. Permanent deletion from the Recycle Bin removes the profile and its attendance history and deletes its face-sample folder.

That recovery is inside the application only. It is not a replacement for a separate backup.

## Backups

Stop the app before copying the complete **data** folder to approved secure storage. Do not email the folder or place it in a public repository. The face model can be regenerated from retained face samples.

## Before using real campus data

- Get approval from the university and explain the purpose to students and faculty.
- Decide who may register people, see attendance, restore profiles and permanently delete data.
- Set a retention period and a process for access, correction and deletion requests.
- Keep backups encrypted and access-controlled.
- Review false matches, false rejections and camera spoofing risks with a non-biometric fallback.
- Do not expose the local server or use this prototype as a shared campus server.

The current app has no login, administrator roles, liveness detection or centralized encrypted storage. Recognition results need human review before they affect official attendance decisions.
