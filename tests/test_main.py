import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from readme_generator_agent.main import handler


@pytest.mark.asyncio
async def test_handler_returns_response():
    """Test that handler accepts messages and returns a response."""
    messages = [{"role": "user", "content": "Hello, how are you?"}]

    # Mock the run_agent function to return a mock response
    mock_response = MagicMock()
    mock_response.run_id = "test-run-id"
    mock_response.status = "COMPLETED"

    # Mock _initialized to skip initialization and run_agent to return our mock
    with (
        patch("readme_generator_agent.main._initialized", True),
        patch("readme_generator_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response),
    ):
        result = await handler(messages)

    # Verify we get a result back
    assert result is not None
    assert result.run_id == "test-run-id"
    assert result.status == "COMPLETED"


@pytest.mark.asyncio
async def test_handler_with_multiple_messages():
    """Test that handler processes multiple messages correctly."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather?"},
    ]

    mock_response = MagicMock()
    mock_response.run_id = "test-run-id-2"

    with (
        patch("readme_generator_agent.main._initialized", True),
        patch("readme_generator_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response) as mock_run,
    ):
        result = await handler(messages)

    # Verify run_agent was called
    mock_run.assert_called_once_with(messages)
    assert result is not None
    assert result.run_id == "test-run-id-2"


@pytest.mark.asyncio
async def test_handler_initialization():
    """Test that handler initializes on first call."""
    messages = [{"role": "user", "content": "Test"}]

    mock_response = MagicMock()

    # Start with _initialized as False to test initialization path
    with (
        patch("readme_generator_agent.main._initialized", False),
        patch("readme_generator_agent.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch("readme_generator_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response) as mock_run,
        patch("readme_generator_agent.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        result = await handler(messages)

        # Verify initialization was called
        mock_init.assert_called_once()
        # Verify run_agent was called
        mock_run.assert_called_once_with(messages)
        # Verify we got a result
        assert result is not None


@pytest.mark.asyncio
async def test_handler_with_readme_generation_query():
    """Test that handler can process a README generation query."""
    messages = [
        {
            "role": "user",
            "content": "Generate a README for https://github.com/agno-agi/agno",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "readme-run-id"
    mock_response.content = "README generated successfully."

    with (
        patch("readme_generator_agent.main._initialized", True),
        patch("readme_generator_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "readme-run-id"
    assert result.content == "README generated successfully."