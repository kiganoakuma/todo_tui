import unittest
import datetime
from task import Task  # Assuming the Task class is in a file named task.py


class TestTask(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.tomorrow = self.today + datetime.timedelta(days=1)

        # Create sample tasks for testing
        self.task_no_due_date = Task(id=1, title="Test task without due date")
        self.task_due_tomorrow = Task(
            id=2, title="Test task due tomorrow", due_date=self.tomorrow
        )
        self.task_overdue = Task(
            id=3, title="Test overdue task", due_date=self.yesterday
        )
        self.task_overdue_completed = Task(
            id=4,
            title="Test overdue but completed task",
            due_date=self.yesterday,
            completed=True,
        )
        self.task_with_all_fields = Task(
            id=5,
            title="Complete task with all fields",
            completed=True,
            priority="high",
            due_date=self.tomorrow,
            category="Work",
            notes="This is a test note",
        )

    def test_initialization(self):
        """Test that Task objects are initialized correctly."""
        # Test required fields
        task = Task(id=1, title="Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")

        # Test default values
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, "medium")
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.category)
        self.assertIsNone(task.notes)

        # Test with all fields
        task = self.task_with_all_fields
        self.assertEqual(task.id, 5)
        self.assertEqual(task.title, "Complete task with all fields")
        self.assertTrue(task.completed)
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.due_date, self.tomorrow)
        self.assertEqual(task.category, "Work")
        self.assertEqual(task.notes, "This is a test note")

    def test_is_overdue(self):
        """Test the is_overdue method."""
        # Task with no due date should not be overdue
        self.assertFalse(self.task_no_due_date.is_overdue())

        # Task due tomorrow should not be overdue
        self.assertFalse(self.task_due_tomorrow.is_overdue())

        # Task due yesterday should be overdue
        self.assertTrue(self.task_overdue.is_overdue())

        # Task due yesterday but completed should not be overdue
        self.assertFalse(self.task_overdue_completed.is_overdue())

    def test_to_dict(self):
        """Test the to_dict method."""
        # Test with all fields
        task_dict = self.task_with_all_fields.to_dict()

        self.assertEqual(task_dict["id"], 5)
        self.assertEqual(task_dict["title"], "Complete task with all fields")
        self.assertTrue(task_dict["completed"])
        self.assertEqual(task_dict["priority"], "high")
        self.assertEqual(task_dict["due_date"], self.tomorrow.isoformat())
        self.assertEqual(task_dict["category"], "Work")
        self.assertEqual(task_dict["notes"], "This is a test note")

        # Test with minimal fields
        task_dict = self.task_no_due_date.to_dict()
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["title"], "Test task without due date")
        self.assertFalse(task_dict["completed"])
        self.assertEqual(task_dict["priority"], "medium")
        self.assertIsNone(task_dict["due_date"])
        self.assertIsNone(task_dict["category"])
        self.assertIsNone(task_dict["notes"])

    def test_from_dict(self):
        """Test the from_dict class method."""
        # Convert a task to dict and back to ensure it works correctly
        original_task = self.task_with_all_fields
        task_dict = original_task.to_dict()
        recreated_task = Task.from_dict(task_dict)

        # Test all fields are preserved
        self.assertEqual(recreated_task.id, original_task.id)
        self.assertEqual(recreated_task.title, original_task.title)
        self.assertEqual(recreated_task.completed, original_task.completed)
        self.assertEqual(recreated_task.priority, original_task.priority)
        self.assertEqual(recreated_task.due_date, original_task.due_date)
        self.assertEqual(recreated_task.category, original_task.category)
        self.assertEqual(recreated_task.notes, original_task.notes)

        # Test with None values
        minimal_dict = {
            "id": 99,
            "title": "Minimal task",
            "completed": False,
            "priority": "low",
            "due_date": None,
            "category": None,
            "notes": None,
        }
        minimal_task = Task.from_dict(minimal_dict)
        self.assertEqual(minimal_task.id, 99)
        self.assertEqual(minimal_task.title, "Minimal task")
        self.assertFalse(minimal_task.completed)
        self.assertEqual(minimal_task.priority, "low")
        self.assertIsNone(minimal_task.due_date)
        self.assertIsNone(minimal_task.category)
        self.assertIsNone(minimal_task.notes)

    def test_roundtrip_serialization(self):
        """Test full serialization roundtrip (Task -> dict -> Task)."""
        # Create tasks with different combinations of fields
        tasks = [
            self.task_no_due_date,
            self.task_due_tomorrow,
            self.task_overdue,
            self.task_overdue_completed,
            self.task_with_all_fields,
        ]

        for original_task in tasks:
            # Convert to dict
            task_dict = original_task.to_dict()
            # Convert back to Task
            recreated_task = Task.from_dict(task_dict)

            # Verify all attributes are the same
            self.assertEqual(recreated_task.id, original_task.id)
            self.assertEqual(recreated_task.title, original_task.title)
            self.assertEqual(recreated_task.completed, original_task.completed)
            self.assertEqual(recreated_task.priority, original_task.priority)
            self.assertEqual(recreated_task.due_date, original_task.due_date)
            self.assertEqual(recreated_task.category, original_task.category)
            self.assertEqual(recreated_task.notes, original_task.notes)

            # Also verify the overdue logic is preserved
            self.assertEqual(recreated_task.is_overdue(), original_task.is_overdue())


if __name__ == "__main__":
    unittest.main()
