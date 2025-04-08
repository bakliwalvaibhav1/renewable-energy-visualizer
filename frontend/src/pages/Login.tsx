import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Navigate } from "react-router-dom";
import { api } from "../library/axios";

export default function Login() {
    const { isAuthenticated, login } = useAuth();
    const navigate = useNavigate();

    const [mode, setMode] = useState<"login" | "register">("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    if (isAuthenticated) {
        return <Navigate to="/dashboard" />;
    }

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const response = await api.post(
                "/auth/login",
                new URLSearchParams({ username: email, password }),
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );

            login(response.data.access_token);
            navigate("/dashboard");
        } catch (err) {
            console.error("Login error:", err);
        }
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        try {
            await api.post("/auth/register", { email, password });

            alert("Registration successful! You can now log in.");
            setMode("login");
        } catch (err) {
            console.error("Register error:", err);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 shadow rounded bg-white">
            {/* Toggle Tabs */}
            <div className="flex justify-center gap-4 mb-6">
                <button
                    type="button"
                    className={`px-4 py-2 rounded ${
                        mode === "login"
                            ? "bg-blue-500 text-white"
                            : "bg-gray-200"
                    }`}
                    onClick={() => setMode("login")}
                >
                    Login
                </button>
                <button
                    type="button"
                    className={`px-4 py-2 rounded ${
                        mode === "register"
                            ? "bg-blue-500 text-white"
                            : "bg-gray-200"
                    }`}
                    onClick={() => setMode("register")}
                >
                    Register
                </button>
            </div>

            {/* Login / Register Form */}
            <form
                onSubmit={mode === "login" ? handleLogin : handleRegister}
                className="space-y-4"
            >
                <input
                    type="email"
                    placeholder="Email"
                    className="w-full p-2 border rounded"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    className="w-full p-2 border rounded"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {mode === "register" && (
                    <input
                        type="password"
                        placeholder="Confirm Password"
                        className="w-full p-2 border rounded"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                )}

                <button
                    type="submit"
                    className="w-full py-2 rounded text-white bg-blue-600 hover:bg-blue-700"
                >
                    {mode === "login" ? "Login" : "Register"}
                </button>
            </form>
        </div>
    );
}
