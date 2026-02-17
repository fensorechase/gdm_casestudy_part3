# GDM Chatbot - Cloud Deployment Requirements

## Functional Requirements
- [ ] All existing features work (login, dashboard, chat, glucose)
- [ ] Chat responses in <3 seconds
- [ ] Support 10 concurrent usersls
- [ ] Data persists across deployments

## Technical Requirements
- [ ] Deploy to Google Cloud Run (us-central1)
- [ ] PostgreSQL database (Cloud SQL, db-f1-micro)
- [ ] HTTPS only
- [ ] Environment variables for secrets
- [ ] Dockerfile for containerization

## Resource Constraints
- **Budget:** <$5 for 1 week
- **Region:** us-central1 (cheapest)
- **Database:** Smallest instance (db-f1-micro, ~$7/month prorated)
- **Cloud Run:** Max 2 instances, 512MB RAM each

## LMIC Optimizations
- [ ] Response payload <50KB
- [ ] Works on 3G (3-5 Mbps)
- [ ] Progressive loading

## Security
- [ ] HTTPS enforced
- [ ] Database password not in code
- [ ] No PHI in logs
- [ ] SQL injection prevention (parameterized queries)

## Success Criteria
- [ ] Public URL accessible
- [ ] 5 test users can login and chat
- [ ] Database persists data
- [ ] Costs <$5 for week
- [ ] Rollback procedure documented