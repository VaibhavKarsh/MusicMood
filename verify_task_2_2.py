"""
Verification script for Task 2.2: Database Models & Schema
"""

import sys
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Import settings and models
from app.config.settings import settings
from app.models import Base, User, MoodEntry, PlaylistRecommendation


def verify_database_models():
    """Verify that database models and tables are correctly created."""
    
    print("=" * 70)
    print("Verifying Database Models & Schema (Task 2.2)")
    print("=" * 70)
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        
        # Check 1: Verify all tables exist
        print("\n[CHECK 1] Verifying tables exist in database...")
        expected_tables = ['users', 'mood_entries', 'playlist_recommendations', 'alembic_version']
        existing_tables = inspector.get_table_names()
        
        all_tables_exist = True
        for table in expected_tables:
            if table in existing_tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' NOT FOUND")
                all_tables_exist = False
        
        if not all_tables_exist:
            print("\n❌ NOT ALL TABLES EXIST")
            return False
        
        # Check 2: Verify User model columns
        print("\n[CHECK 2] Verifying User model columns...")
        user_columns = {col['name'] for col in inspector.get_columns('users')}
        expected_user_cols = {
            'id', 'username', 'email', 'hashed_password', 
            'is_active', 'is_superuser', 
            'spotify_access_token', 'spotify_refresh_token', 'spotify_token_expires_at',
            'created_at', 'updated_at'
        }
        
        if expected_user_cols.issubset(user_columns):
            print(f"✓ User model has all expected columns: {len(expected_user_cols)} columns")
            print(f"  Columns: {', '.join(sorted(expected_user_cols))}")
        else:
            missing = expected_user_cols - user_columns
            print(f"✗ User model missing columns: {missing}")
            return False
        
        # Check 3: Verify MoodEntry model columns
        print("\n[CHECK 3] Verifying MoodEntry model columns...")
        mood_columns = {col['name'] for col in inspector.get_columns('mood_entries')}
        expected_mood_cols = {
            'id', 'user_id', 'mood_text', 'detected_emotion', 'emotion_scores',
            'confidence_score', 'weather_data', 'time_of_day', 
            'location_context', 'activity_context',
            'created_at', 'updated_at'
        }
        
        if expected_mood_cols.issubset(mood_columns):
            print(f"✓ MoodEntry model has all expected columns: {len(expected_mood_cols)} columns")
            print(f"  Columns: {', '.join(sorted(expected_mood_cols))}")
        else:
            missing = expected_mood_cols - mood_columns
            print(f"✗ MoodEntry model missing columns: {missing}")
            return False
        
        # Check 4: Verify PlaylistRecommendation model columns
        print("\n[CHECK 4] Verifying PlaylistRecommendation model columns...")
        playlist_columns = {col['name'] for col in inspector.get_columns('playlist_recommendations')}
        expected_playlist_cols = {
            'id', 'user_id', 'mood_entry_id', 'playlist_name', 'description',
            'track_ids', 'track_details', 'genre_distribution', 'audio_features_avg',
            'reasoning', 'agent_used', 'feedback_score', 'was_listened',
            'spotify_playlist_id', 'created_at', 'updated_at'
        }
        
        if expected_playlist_cols.issubset(playlist_columns):
            print(f"✓ PlaylistRecommendation model has all expected columns: {len(expected_playlist_cols)} columns")
            print(f"  Columns: {', '.join(sorted(expected_playlist_cols))}")
        else:
            missing = expected_playlist_cols - playlist_columns
            print(f"✗ PlaylistRecommendation model missing columns: {missing}")
            return False
        
        # Check 5: Verify foreign key relationships
        print("\n[CHECK 5] Verifying foreign key relationships...")
        
        # MoodEntry -> User
        mood_fks = inspector.get_foreign_keys('mood_entries')
        mood_fk_to_user = any(
            fk['referred_table'] == 'users' and 'user_id' in fk['constrained_columns']
            for fk in mood_fks
        )
        
        if mood_fk_to_user:
            print("✓ MoodEntry has foreign key to User (user_id)")
        else:
            print("✗ MoodEntry foreign key to User NOT FOUND")
            return False
        
        # PlaylistRecommendation -> User
        playlist_fks = inspector.get_foreign_keys('playlist_recommendations')
        playlist_fk_to_user = any(
            fk['referred_table'] == 'users' and 'user_id' in fk['constrained_columns']
            for fk in playlist_fks
        )
        
        if playlist_fk_to_user:
            print("✓ PlaylistRecommendation has foreign key to User (user_id)")
        else:
            print("✗ PlaylistRecommendation foreign key to User NOT FOUND")
            return False
        
        # PlaylistRecommendation -> MoodEntry
        playlist_fk_to_mood = any(
            fk['referred_table'] == 'mood_entries' and 'mood_entry_id' in fk['constrained_columns']
            for fk in playlist_fks
        )
        
        if playlist_fk_to_mood:
            print("✓ PlaylistRecommendation has foreign key to MoodEntry (mood_entry_id)")
        else:
            print("✗ PlaylistRecommendation foreign key to MoodEntry NOT FOUND")
            return False
        
        # Check 6: Verify indexes
        print("\n[CHECK 6] Verifying database indexes...")
        
        # User indexes
        user_indexes = {idx['name'] for idx in inspector.get_indexes('users')}
        if 'ix_users_username' in user_indexes and 'ix_users_email' in user_indexes:
            print(f"✓ User indexes present: {len(user_indexes)} indexes")
        else:
            print(f"✗ User indexes incomplete: {user_indexes}")
            return False
        
        # MoodEntry indexes
        mood_indexes = {idx['name'] for idx in inspector.get_indexes('mood_entries')}
        if 'idx_mood_user_created' in mood_indexes:
            print(f"✓ MoodEntry indexes present: {len(mood_indexes)} indexes")
        else:
            print(f"✗ MoodEntry indexes incomplete: {mood_indexes}")
            return False
        
        # PlaylistRecommendation indexes
        playlist_indexes = {idx['name'] for idx in inspector.get_indexes('playlist_recommendations')}
        if 'idx_playlist_user_created' in playlist_indexes:
            print(f"✓ PlaylistRecommendation indexes present: {len(playlist_indexes)} indexes")
        else:
            print(f"✗ PlaylistRecommendation indexes incomplete: {playlist_indexes}")
            return False
        
        # Check 7: Verify Alembic migration applied
        print("\n[CHECK 7] Verifying Alembic migration applied...")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        result = session.execute(text("SELECT version_num FROM alembic_version"))
        version = result.fetchone()
        
        if version:
            print(f"✓ Alembic migration applied: version {version[0]}")
        else:
            print("✗ No Alembic version found")
            return False
        
        session.close()
        
        # Check 8: Test model instantiation
        print("\n[CHECK 8] Testing model instantiation...")
        
        try:
            # Test User model
            user = User(
                username="testuser",
                email="test@example.com",
                hashed_password="hashedpass123",
                is_active=True,
                is_superuser=False
            )
            print(f"✓ User model instantiates correctly: {user}")
            
            # Test MoodEntry model
            mood = MoodEntry(
                user_id=1,
                mood_text="Feeling happy today",
                detected_emotion="happy",
                confidence_score=0.95,
                time_of_day="morning"
            )
            print(f"✓ MoodEntry model instantiates correctly: {mood}")
            
            # Test PlaylistRecommendation model
            playlist = PlaylistRecommendation(
                user_id=1,
                mood_entry_id=1,
                playlist_name="Happy Morning Mix",
                description="Upbeat songs for your morning",
                track_ids=["track1", "track2"],
                track_details=[{"name": "Song 1"}],
                reasoning="Selected based on happy mood",
                agent_used="coordinator"
            )
            print(f"✓ PlaylistRecommendation model instantiates correctly")
            
        except Exception as e:
            print(f"✗ Model instantiation failed: {e}")
            return False
        
        print("\n" + "=" * 70)
        print("✅ ALL CHECKS PASSED - Task 2.2 Complete")
        print("=" * 70)
        print("\nSummary:")
        print("  • Database tables created successfully")
        print("  • All model columns present")
        print("  • Foreign key relationships established")
        print("  • Indexes created for performance")
        print("  • Alembic migration system working")
        print("  • Models instantiate correctly")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_database_models()
    sys.exit(0 if success else 1)
