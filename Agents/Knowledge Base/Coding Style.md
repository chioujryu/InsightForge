# ZURU Melon Coding Style Guide

**Version:** 1.0  
**Last Updated:** 2025-29-10

## Introduction

Welcome to the ZURU Melon Coding Style Guide! At ZURU Melon, we help our clients succeed by harnessing the power of AI and delivering robust, user-friendly web applications. Maintaining high-quality, consistent code ensures reliability, scalability, and ease of collaboration.

This guide outlines our best practices for writing software, currently focusing on Python (backend) and TypeScript (frontend). All developers are expected to read, understand, and adhere to these conventions.

---

## General Principles

- **Clarity over Cleverness:** Code should be easy to read and understand.
- **Consistency:** Stick to our conventions, even if you have personal preferences.
- **Documentation:** Good code is well-documented. Leave meaningful comments and docstrings.
- **Testing:** All features must include unit and integration tests.
- **AI Responsibility:** When using AI models, ensure ethical handling of data and model results.

---

## Python Coding Standards

### 1. Formatting

- Follow [PEP 8](https://pep8.org/) as the basic style guide.
- Use 4 spaces per indentation level. Never use tabs.
- Maximum line length: 100 characters.
- Always use UTF-8 encoding.
- Prefer single quotes for strings unless double quotes improve readability.

### 2. Naming Conventions

- **Variables and functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `ALL_CAPS`
- Private variables/functions/methods: Prefix with `_`

### 3. Imports

- Standard library imports first, third-party libraries second, local modules last.
- One import per line.
- Avoid wildcard imports.

    ```python
    # Correct:
    import os
    import numpy as np
    from zuru_melon.utils import ai_helper
    ```

### 4. Type Annotations

- Use type hints for all function arguments and return types.
- Use [`mypy`](http://mypy-lang.org/) for static type checking.

    ```python
    def classify_image(image: np.ndarray) -> str:
        ...
    ```

### 5. Docstrings & Comments

- All public modules, classes, functions, and methods require docstrings in [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- Use comments thoughtfully—don't state the obvious.

    ```python
    def add(a: int, b: int) -> int:
        """Add two integers and return the result."""
        return a + b
    ```

### 6. Exception Handling

- Be specific in exception handling.
- Never use bare `except:`—always specify the exception.

    ```python
    try:
        process_data()
    except ValueError as e:
        logger.error(f"Value error: {e}")
    ```

### 7. AI Integration

- Never hard-code model weights—use configuration or environment variables.
- Always log AI model input/output for traceability (excluding sensitive data).
- Be explicit about the version of AI models in use.

---

## TypeScript Coding Standards

### 1. Formatting

- Use [Prettier](https://prettier.io/) for automatic formatting.
- 2 spaces per indentation level.
- Maximum line length: 100 characters.

### 2. Naming Conventions

- **Variables/functions:** `camelCase`
- **Classes:** `PascalCase`
- **Constants:** `ALL_CAPS`
- Private members: Prefix with `_`

### 3. Imports

- Use ES6 modules (`import/export`).
- Import only what is needed—no wildcard or namespace imports.

    ```typescript
    import { useState } from 'react';
    ```

### 4. Types

- Always type function arguments and return values.
- Avoid using `any`.
- Use interfaces over types for object definitions when possible.

    ```typescript
    interface UserProfile {
      id: number;
      name: string;
    }

    function greet(user: UserProfile): string {
      return `Hello, ${user.name}!`;
    }
    ```

### 5. Comments & Documentation

- Use JSDoc for public functions and classes.
- Write comments only where necessary.

    ```typescript
    /**
     * Calculate the sum of two numbers
     */
    function sum(a: number, b: number): number {
      return a + b;
    }
    ```

### 6. Error Handling

- Handle errors through try/catch, especially with async functions.
- Display user-friendly messages for caught errors.

### 7. React Guidelines

- Use [functional components](https://reactjs.org/docs/components-and-props.html) only.
- Separate logic and presentation (custom hooks encouraged).
- All props and states must be explicitly typed.

    ```typescript
    interface ButtonProps {
      onClick: () => void;
      label: string;
    }

    const Button: React.FC<ButtonProps> = ({ onClick, label }) => (
      <button onClick={onClick}>{label}</button>
    );
    ```

---

## Testing Standards

- All new features require unit and integration tests.
- Use `pytest` for Python and `jest`/`react-testing-library` for TypeScript.
- Target 90% code coverage for all modules.
- Structure tests to mirror the main project structure.
- For AI code, implement both correctness and bias/robustness tests when possible.

---

## Security & Confidentiality

- Never commit secrets or sensitive data.
- Sanitize all user inputs on both frontend and backend.
- Review code for possible data leaks, especially in AI model outputs.

---

## Automation & Tooling

- **Linters:**
    - Python: `flake8`, `black`, `mypy`
    - TypeScript: `eslint`, `prettier`
- **CI/CD:** All merges must pass the full test/lint suite prior to deployment.
- **Pre-commit hooks:** Set up and maintained in [`.pre-commit-config.yaml`](https://pre-commit.com/).

---

## Code Review Process

1. Submit a pull request with a clear description.
2. Another developer **must** review and approve before merging.
3. Address all review comments and suggestions.
4. All code must pass CI/CD checks before merging.

---

## Conclusion

Following these guidelines ensures our codebase remains a valuable asset for every ZURU Melon engineer and client. If you have feedback, questions, or suggestions, reach out to the Engineering Leads or create an issue in our internal documentation portal.

**Let’s code the Melon way—clear, consistent, and clever when it counts!**

